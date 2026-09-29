"""Pydantic schemas for query request and response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for POST /query endpoint."""

    query: str = Field(..., description="Search query string")
    top_k_retrieve: Optional[int] = Field(
        None, description="Number of candidate chunks to retrieve per search method (dense/BM25)"
    )
    top_k_rerank: Optional[int] = Field(
        None, description="Number of final top reranked results to return"
    )
    use_reranker: bool = Field(
        True, description="Whether to apply cross-encoder reranking after RRF fusion"
    )


class SearchResultChunk(BaseModel):
    """Individual retrieval result chunk model."""

    chunk_id: str = Field(
        ..., description="Unique chunk identifier formatted as {doc_id}_{chunk_index}"
    )
    doc_id: str = Field(..., description="Source document identifier")
    text: str = Field(..., description="Text chunk content")
    score: float = Field(
        ..., description="Relevance score (RRF fused score or cross-encoder score)"
    )
    rank: int = Field(..., description="Position in final returned results (1-indexed)")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata associated with chunk"
    )


class QueryResponse(BaseModel):
    """Response model for POST /query endpoint."""

    query: str = Field(..., description="Original search query string")
    results: List[SearchResultChunk] = Field(..., description="Ordered list of top relevant chunks")
    total_results: int = Field(..., description="Number of results returned")
