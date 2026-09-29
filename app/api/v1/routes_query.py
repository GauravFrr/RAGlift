"""Thin API route for hybrid query retrieval."""

from fastapi import APIRouter, Depends, status

from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="", tags=["Query"])


def get_retrieval_service() -> RetrievalService:
    """Dependency provider for RetrievalService."""
    return RetrievalService()


@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_retrieval(
    request: QueryRequest,
    service: RetrievalService = Depends(get_retrieval_service),
) -> QueryResponse:
    """Execute hybrid retrieval + RRF fusion + cross-encoder reranking query.

    Delegates completely to RetrievalService.
    """
    return service.query(request)
