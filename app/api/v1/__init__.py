"""API v1 routes module initialization."""

from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_ingest import router as ingest_router
from app.api.v1.routes_query import router as query_router

__all__ = ["health_router", "ingest_router", "query_router"]
