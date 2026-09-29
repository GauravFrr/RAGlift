"""Healthcheck endpoint for monitoring and Docker probes."""

from fastapi import APIRouter, status

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    """Liveness check returning service status."""
    return {"status": "ok", "service": "RAGLift", "version": "1.0.0"}
