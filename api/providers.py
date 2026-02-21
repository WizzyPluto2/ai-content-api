"""Provider listing endpoint."""

from fastapi import APIRouter

from providers import list_providers

router = APIRouter()


@router.get("/providers")
async def get_providers():
    """List all available LLM providers and their status."""
    return {"providers": list_providers()}
