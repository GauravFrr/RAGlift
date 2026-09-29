"""Ingestion service for RAGLift.

Orchestrates text chunking, vector embedding, BM25 indexing, ChromaDB persistence,
and append-only JSONL audit logging.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.core.exceptions import IngestionException
from app.core.logging import logger
from app.embeddings import get_embedding_provider
from app.embeddings.base import EmbeddingProvider
from app.retrieval.bm25 import BM25Index
from app.retrieval.dense import DenseRetriever
from app.schemas.ingest import DocumentInput, IngestResponse


class IngestionService:
    """Service encapsulating end-to-end document chunking and indexing pipeline."""

    def __init__(
        self,
        provider: Optional[EmbeddingProvider] = None,
        bm25_index: Optional[BM25Index] = None,
        dense_retriever: Optional[DenseRetriever] = None,
    ):
        """Initialize IngestionService with dependencies."""
        self.provider = provider or get_embedding_provider()
        self.bm25_index = bm25_index or BM25Index()
        self.dense_retriever = dense_retriever or DenseRetriever(provider=self.provider)

    def _chunk_text(
        self, text: str, chunk_size: int, chunk_overlap: int
    ) -> List[str]:
        """Split text string into overlapping token/word chunks.

        Args:
            text: Raw input text content.
            chunk_size: Target words per chunk.
            chunk_overlap: Number of overlapping words between consecutive chunks.

        Returns:
            List of chunk text strings.
        """
        words = text.split()
        if not words:
            return []

        if len(words) <= chunk_size:
            return [" ".join(words)]

        chunks = []
        step = max(1, chunk_size - chunk_overlap)
        for i in range(0, len(words), step):
            chunk_words = words[i : i + chunk_size]
            if chunk_words:
                chunks.append(" ".join(chunk_words))
            if i + chunk_size >= len(words):
                break

        return chunks

    def _log_ingestion_entry(
        self, doc_id: str, source_path: str, chunk_count: int, ingested_at: str
    ) -> None:
        """Append entry to jsonl ingestion log file."""
        log_path = settings.INGESTION_LOG_PATH
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        entry = {
            "doc_id": doc_id,
            "source_path": source_path,
            "chunk_count": chunk_count,
            "ingested_at": ingested_at,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def ingest_documents(
        self,
        documents: List[DocumentInput],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> IngestResponse:
        """Process, chunk, embed, and index a batch of input documents.

        Args:
            documents: List of DocumentInput objects.
            chunk_size: Optional chunk size override.
            chunk_overlap: Optional chunk overlap override.

        Returns:
            IngestResponse with processing stats.
        """
        if not documents:
            raise IngestionException("Cannot ingest an empty document list.")

        size = chunk_size or settings.CHUNK_SIZE
        overlap = chunk_overlap or settings.CHUNK_OVERLAP

        all_chunk_ids: List[str] = []
        all_chunk_texts: List[str] = []
        all_metadatas: List[Dict[str, Any]] = []

        now_iso = datetime.now(timezone.utc).isoformat()

        for doc in documents:
            chunks = self._chunk_text(doc.text, chunk_size=size, chunk_overlap=overlap)
            source_path = (
                doc.metadata.get("source_path", doc.doc_id) if doc.metadata else doc.doc_id
            )

            for idx, chunk_text in enumerate(chunks):
                chunk_id = f"{doc.doc_id}_{idx}"
                meta = {
                    "doc_id": doc.doc_id,
                    "chunk_index": idx,
                    "source_path": source_path,
                    "ingested_at": now_iso,
                }
                if doc.metadata:
                    meta.update({k: str(v) for k, v in doc.metadata.items() if k not in meta})

                all_chunk_ids.append(chunk_id)
                all_chunk_texts.append(chunk_text)
                all_metadatas.append(meta)

            self._log_ingestion_entry(
                doc_id=doc.doc_id,
                source_path=source_path,
                chunk_count=len(chunks),
                ingested_at=now_iso,
            )

        if not all_chunk_texts:
            raise IngestionException("No valid text chunks generated from input documents.")

        logger.info(
            "Generating embeddings for %d chunks across %d documents...",
            len(all_chunk_texts),
            len(documents),
        )
        embeddings = self.provider.embed_documents(all_chunk_texts)

        # Index in BM25
        self.bm25_index.add_chunks(
            chunk_ids=all_chunk_ids, documents=all_chunk_texts, metadatas=all_metadatas
        )

        # Index in ChromaDB
        self.dense_retriever.add_chunks(
            chunk_ids=all_chunk_ids,
            embeddings=embeddings,
            documents=all_chunk_texts,
            metadatas=all_metadatas,
        )

        return IngestResponse(
            status="success",
            documents_processed=len(documents),
            total_chunks=len(all_chunk_ids),
            ingested_at=now_iso,
        )
