"""Content template system."""

from templates.registry import TEMPLATES


def get_template(template_id: str):
    """Get a template by ID."""
    if template_id not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(f"Template '{template_id}' not found. Available: {available}")
    return TEMPLATES[template_id]


def list_templates() -> list[dict]:
    """List all available templates."""
    return [t.model_dump() for t in TEMPLATES.values()]


__all__ = ["get_template", "list_templates"]
