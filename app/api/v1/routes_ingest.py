"""Thin API route for document ingestion."""

from fastapi import APIRouter, Depends, status

from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="", tags=["Ingestion"])


def get_ingestion_service() -> IngestionService:
    """Dependency provider for IngestionService."""
    return IngestionService()


@router.post("/ingest", response_model=IngestResponse, status_code=status.HTTP_200_OK)
async def ingest_documents(
    request: IngestRequest,
    service: IngestionService = Depends(get_ingestion_service),
) -> IngestResponse:
    """Ingest documents, chunk, embed, and update BM25 and vector stores.

    Delegates completely to IngestionService.
    """
    return service.ingest_documents(
        documents=request.documents,
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
    )
