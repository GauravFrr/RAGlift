"""Custom exception classes and HTTP exception handlers for RAGLift."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.logging import logger


class RAGLiftException(Exception):
    """Base exception class for all custom RAGLift errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class IngestionException(RAGLiftException):
    """Raised when document chunking, embedding, or indexing fails."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class RetrievalException(RAGLiftException):
    """Raised when vector search, BM25 search, fusion, or reranking fails."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IndexNotFoundException(RAGLiftException):
    """Raised when trying to query an uninitialized or empty index."""

    def __init__(
        self,
        message: str = (
            "Retrieval index is empty or not initialized. Please ingest documents first."
        ),
    ):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


async def raglift_exception_handler(request: Request, exc: RAGLiftException) -> JSONResponse:
    """FastAPI global exception handler for custom RAGLift exceptions."""
    logger.error("Handled RAGLiftException: path=%s message=%s", request.url.path, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": exc.__class__.__name__},
    )
