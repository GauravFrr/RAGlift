"""FastAPI Application Factory for RAGLift.

Mounts API v1 routes and global exception handlers. Contains zero business logic.
"""

from fastapi import FastAPI

from app.api.v1 import health_router, ingest_router, query_router
from app.core.exceptions import RAGLiftException, raglift_exception_handler


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="RAGLift — Production RAG Starter Kit",
        description=(
            "Production-grade hybrid search (BM25 + vector similarity) "
            "with Reciprocal Rank Fusion and Cross-Encoder reranking."
        ),
        version="1.0.0",
    )

    # Register global exception handlers
    app.add_exception_handler(RAGLiftException, raglift_exception_handler)

    # Mount API routers under /api/v1 and top level
    app.include_router(health_router)
    app.include_router(ingest_router, prefix="/api/v1")
    app.include_router(query_router, prefix="/api/v1")

    # Top-level route aliases for convenience
    app.include_router(ingest_router)
    app.include_router(query_router)

    return app


app = create_app()
