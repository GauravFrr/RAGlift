"""Retrieval service for RAGLift.

Orchestrates the multi-stage hybrid retrieval pipeline:
1. BM25 keyword search (candidate retrieval)
2. Dense vector search via ChromaDB (candidate retrieval)
3. Reciprocal Rank Fusion (RRF candidate merging)
4. Cross-Encoder reranking (final scoring and ordering)
"""

from typing import Optional

from app.core.config import settings
from app.core.exceptions import IndexNotFoundException, RetrievalException
from app.core.logging import logger
from app.embeddings import get_embedding_provider
from app.embeddings.base import EmbeddingProvider
from app.retrieval.bm25 import BM25Index
from app.retrieval.dense import DenseRetriever
from app.retrieval.fusion import rrf_fuse
from app.retrieval.reranker import Reranker
from app.schemas.query import QueryRequest, QueryResponse, SearchResultChunk


class RetrievalService:
    """Service encapsulating hybrid retrieval, RRF fusion, and cross-encoder reranking."""

    def __init__(
        self,
        provider: Optional[EmbeddingProvider] = None,
        bm25_index: Optional[BM25Index] = None,
        dense_retriever: Optional[DenseRetriever] = None,
        reranker: Optional[Reranker] = None,
    ):
        """Initialize RetrievalService with dependencies."""
        self.provider = provider or get_embedding_provider()
        self.bm25_index = bm25_index or BM25Index()
        self.dense_retriever = dense_retriever or DenseRetriever(provider=self.provider)
        self.reranker = reranker or Reranker()

    def query(self, request: QueryRequest) -> QueryResponse:
        """Execute multi-stage hybrid retrieval for a search query.

        Args:
            request: QueryRequest specifying query string and retrieval parameters.

        Returns:
            QueryResponse containing ordered SearchResultChunk objects.
        """
        query_text = request.query.strip()
        if not query_text:
            raise RetrievalException("Query string cannot be empty.")

        top_k_retrieve = request.top_k_retrieve or settings.TOP_K_RETRIEVE
        top_k_rerank = request.top_k_rerank or settings.TOP_K_RERANK

        # Check if index has documents
        if not self.bm25_index.chunk_ids and self.dense_retriever.count() == 0:
            raise IndexNotFoundException()

        # Step 1: BM25 Keyword Search
        bm25_candidates = self.bm25_index.search(query=query_text, top_k=top_k_retrieve)
        logger.debug(
            "BM25 retrieved %d candidates for query '%s'", len(bm25_candidates), query_text
        )

        # Step 2: Dense Vector Search
        dense_candidates = self.dense_retriever.search(
            query=query_text, provider=self.provider, top_k=top_k_retrieve
        )
        logger.debug("Dense vector search retrieved %d candidates", len(dense_candidates))

        # Step 3: Reciprocal Rank Fusion (RRF)
        fused_candidates = rrf_fuse(
            bm25_results=bm25_candidates,
            dense_results=dense_candidates,
            top_k=top_k_retrieve,
        )
        logger.debug("RRF fusion yielded %d unique candidate chunks", len(fused_candidates))

        if not fused_candidates:
            return QueryResponse(query=query_text, results=[], total_results=0)

        # Step 4: Optional Cross-Encoder Reranking
        if request.use_reranker:
            final_candidates = self.reranker.rerank(
                query=query_text, candidates=fused_candidates, top_k=top_k_rerank
            )
            logger.debug("Cross-encoder reranking returned top %d chunks", len(final_candidates))
        else:
            final_candidates = fused_candidates[:top_k_rerank]

        # Format into SearchResultChunk Pydantic models
        results = []
        for rank_idx, (chunk_id, score, text, metadata) in enumerate(final_candidates, start=1):
            doc_id = metadata.get("doc_id", chunk_id.split("_")[0])
            results.append(
                SearchResultChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    text=text,
                    score=float(score),
                    rank=rank_idx,
                    metadata=metadata,
                )
            )

        return QueryResponse(query=query_text, results=results, total_results=len(results))
