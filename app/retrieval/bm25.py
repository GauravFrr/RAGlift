"""BM25 keyword retrieval engine for RAGLift.

Uses rank_bm25 (BM25Okapi) for term-based lexical retrieval over document chunks.
Persists index to disk as a pickle file so the BM25 index survives restarts
without re-ingesting the entire corpus.
"""

import os
import pickle
import re
from typing import Any, Dict, List, Tuple

from rank_bm25 import BM25Okapi

from app.core.config import settings
from app.core.logging import logger


class BM25Index:
    """In-memory BM25 index with persistence to disk."""

    def __init__(self, index_path: str = None):
        """Initialize BM25 index with target file path for serialization."""
        self.index_path = index_path or settings.BM25_INDEX_PATH
        self.chunk_ids: List[str] = []
        self.documents: List[str] = []
        self.metadatas: List[Dict[str, Any]] = []
        self.bm25: BM25Okapi = None
        self._load()

    def _tokenize(self, text: str) -> List[str]:
        """Simple English tokenizer splitting on alphanumeric characters.

        Normalizes to lowercase for exact token matching.
        """
        return re.findall(r"\w+", text.lower())

    def _load(self) -> None:
        """Load index state from pickle if it exists on disk."""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "rb") as f:
                    data = pickle.load(f)
                    self.chunk_ids = data.get("chunk_ids", [])
                    self.documents = data.get("documents", [])
                    self.metadatas = data.get("metadatas", [])
                    corpus_tokens = [self._tokenize(doc) for doc in self.documents]
                    if corpus_tokens:
                        self.bm25 = BM25Okapi(corpus_tokens)
                logger.info(
                    "Loaded BM25 index from %s (%d chunks)", self.index_path, len(self.chunk_ids)
                )
            except Exception as e:
                logger.warning(
                    "Failed to load existing BM25 index from %s: %s", self.index_path, str(e)
                )
                self._reset_in_memory()
        else:
            self._reset_in_memory()

    def _reset_in_memory(self) -> None:
        """Initialize clean empty state in memory."""
        self.chunk_ids = []
        self.documents = []
        self.metadatas = []
        self.bm25 = None

    def save(self) -> None:
        """Persist BM25 index metadata and documents to disk."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump(
                {
                    "chunk_ids": self.chunk_ids,
                    "documents": self.documents,
                    "metadatas": self.metadatas,
                },
                f,
            )
        logger.info("Saved BM25 index to %s (%d chunks)", self.index_path, len(self.chunk_ids))

    def add_chunks(
        self, chunk_ids: List[str], documents: List[str], metadatas: List[Dict[str, Any]]
    ) -> None:
        """Add new document chunks to the BM25 index and rebuild internal model.

        Args:
            chunk_ids: Unique chunk identifiers.
            documents: Text contents of chunks.
            metadatas: Chunk metadata dictionaries.
        """
        # Append new entries
        self.chunk_ids.extend(chunk_ids)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)

        # Re-tokenize full corpus and rebuild BM25Okapi instance
        tokenized_corpus = [self._tokenize(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)
        self.save()

    def clear(self) -> None:
        """Clear the BM25 index in memory and remove disk persistence file."""
        self._reset_in_memory()
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
            logger.info("Deleted BM25 index file at %s", self.index_path)

    def search(self, query: str, top_k: int = 50) -> List[Tuple[str, float, str, Dict[str, Any]]]:
        """Search the BM25 index for top-k matching chunks.

        Why BM25 keyword search is essential in hybrid retrieval:
        Vector embeddings excel at semantic similarity but frequently miss exact keyword
        matches (e.g. error codes, specific domain terminology, function names, SKU numbers).
        BM25 ensures exact-match signals are preserved and fed into the fusion pipeline.

        Args:
            query: Search query string.
            top_k: Number of candidates to return.

        Returns:
            List of tuples: (chunk_id, bm25_score, document_text, metadata)
        """
        if not self.bm25 or not self.chunk_ids:
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        # Sort indices by score descending
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            # Only include chunks with positive BM25 relevance score
            if score > 0.0:
                results.append(
                    (self.chunk_ids[idx], score, self.documents[idx], self.metadatas[idx])
                )

        return results
