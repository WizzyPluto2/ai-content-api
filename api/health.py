"""Health check endpoint."""

from fastapi import APIRouter

from providers import list_providers

router = APIRouter()


@router.get("/health")
async def health_check():
    """System health check with provider status."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "providers": list_providers(),
    }
