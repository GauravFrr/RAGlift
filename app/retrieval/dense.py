"""Dense vector retrieval engine for RAGLift using ChromaDB.

Handles vector persistence and vector similarity retrieval over text chunk embeddings.
"""

import os
from typing import Any, Dict, List, Tuple

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.core.logging import logger
from app.embeddings.base import EmbeddingProvider


class DenseRetriever:
    """Vector database retrieval manager wrapping ChromaDB."""

    COLLECTION_NAME = "chunks"

    def __init__(self, chroma_path: str = None, provider: EmbeddingProvider = None):
        """Initialize ChromaDB client and collection.

        Args:
            chroma_path: Path to local ChromaDB persistent directory.
            provider: EmbeddingProvider instance used for query embedding.
        """
        self.chroma_path = chroma_path or settings.CHROMA_PATH
        os.makedirs(self.chroma_path, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.chroma_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        self.provider = provider

    def add_chunks(
        self,
        chunk_ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """Add or update chunk vectors in the ChromaDB collection.

        Args:
            chunk_ids: Unique chunk identifiers.
            embeddings: Vector embeddings for each chunk.
            documents: Raw text of chunks.
            metadatas: Metadata dictionaries for each chunk.
        """
        if not chunk_ids:
            return

        self.collection.upsert(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
        logger.info("Upserted %d vector chunks to ChromaDB at %s", len(chunk_ids), self.chroma_path)

    def clear(self) -> None:
        """Clear all entries from ChromaDB collection."""
        try:
            self.client.delete_collection(self.COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Cleared ChromaDB collection '%s'", self.COLLECTION_NAME)
        except Exception as e:
            logger.warning("Error clearing ChromaDB collection: %s", str(e))

    def count(self) -> int:
        """Return total number of chunks stored in ChromaDB."""
        return self.collection.count()

    def search(
        self, query: str, provider: EmbeddingProvider, top_k: int = 50
    ) -> List[Tuple[str, float, str, Dict[str, Any]]]:
        """Search ChromaDB for top-k dense vector matches.

        Why dense retrieval is essential in hybrid retrieval:
        Dense vector retrieval captures deep semantic intent and paraphrasing even when
        the exact vocabulary differs between query and document.

        Args:
            query: Search query string.
            provider: EmbeddingProvider to embed the query vector.
            top_k: Number of candidate matches to retrieve.

        Returns:
            List of tuples: (chunk_id, similarity_score, document_text, metadata)
        """
        if self.collection.count() == 0:
            return []

        # Embed query text
        query_vector = provider.embed_query(query)

        # Execute vector query against ChromaDB
        query_k = min(top_k, self.collection.count())
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=query_k,
            include=["documents", "metadatas", "distances"],
        )

        if not results or not results["ids"] or not results["ids"][0]:
            return []

        ids = results["ids"][0]
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(ids)
        documents = results["documents"][0] if results.get("documents") else [""] * len(ids)
        metadatas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(ids)

        candidates = []
        for cid, dist, doc, meta in zip(ids, distances, documents, metadatas):
            # ChromaDB cosine distance range is [0, 2]. Similarity = 1 - distance.
            similarity_score = 1.0 - float(dist)
            candidates.append((cid, similarity_score, doc, meta))

        return candidates
