"""Template listing endpoints."""

from fastapi import APIRouter, HTTPException

from templates import get_template, list_templates

router = APIRouter()


@router.get("/templates")
async def get_all_templates():
    """List all available content templates."""
    return {"templates": list_templates()}


@router.get("/templates/{template_id}")
async def get_template_detail(template_id: str):
    """Get detailed information about a specific template."""
    try:
        template = get_template(template_id)
        return template.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
