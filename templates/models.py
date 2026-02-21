"""Pydantic models for content templates."""

from pydantic import BaseModel


class TemplateField(BaseModel):
    """A single input field for a content template."""

    name: str
    label: str
    type: str = "text"  # text, textarea, select, number
    required: bool = True
    placeholder: str = ""
    default: str = ""
    options: list[str] | None = None


class ContentTemplate(BaseModel):
    """A content generation template."""

    id: str
    name: str
    description: str
    category: str  # marketing, social, seo, email, video
    icon: str = ""
    fields: list[TemplateField]
    system_prompt: str
    user_prompt_template: str
    output_format: str = "markdown"
    example_output: str = ""
