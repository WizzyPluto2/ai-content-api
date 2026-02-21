"""Tests for the template system."""

import pytest

from templates import get_template, list_templates
from templates.models import ContentTemplate, TemplateField


class TestTemplateModels:
    """Test Pydantic template models."""

    def test_template_field_defaults(self):
        field = TemplateField(name="test", label="Test")
        assert field.type == "text"
        assert field.required is True
        assert field.placeholder == ""
        assert field.options is None

    def test_template_field_with_options(self):
        field = TemplateField(
            name="tone",
            label="Tone",
            type="select",
            options=["casual", "formal"],
        )
        assert field.type == "select"
        assert len(field.options) == 2

    def test_content_template_creation(self):
        template = ContentTemplate(
            id="test",
            name="Test Template",
            description="A test",
            category="test",
            fields=[TemplateField(name="topic", label="Topic")],
            system_prompt="You are a test.",
            user_prompt_template="Write about {topic}",
        )
        assert template.id == "test"
        assert template.output_format == "markdown"


class TestTemplateRegistry:
    """Test template registry functions."""

    def test_list_templates_not_empty(self):
        templates = list_templates()
        assert len(templates) >= 8

    def test_list_templates_returns_dicts(self):
        templates = list_templates()
        for t in templates:
            assert isinstance(t, dict)
            assert "id" in t
            assert "name" in t
            assert "fields" in t

    def test_get_template_blog_post(self):
        template = get_template("blog-post")
        assert template.id == "blog-post"
        assert template.category == "marketing"
        assert any(f.name == "topic" for f in template.fields)

    def test_get_template_social_media(self):
        template = get_template("social-media")
        assert template.id == "social-media"
        assert any(f.name == "platform" for f in template.fields)

    def test_get_template_not_found(self):
        with pytest.raises(ValueError, match="not found"):
            get_template("nonexistent-template")

    def test_all_templates_have_required_fields(self):
        for t in list_templates():
            template = get_template(t["id"])
            assert template.system_prompt, f"{t['id']} missing system_prompt"
            assert template.user_prompt_template, f"{t['id']} missing user_prompt_template"
            assert len(template.fields) > 0, f"{t['id']} has no fields"

    def test_template_prompt_interpolation(self):
        template = get_template("blog-post")
        variables = {
            "topic": "Python testing",
            "tone": "casual",
            "word_count": "500",
            "keywords": "pytest, unittest",
        }
        prompt = template.user_prompt_template.format(**variables)
        assert "Python testing" in prompt
        assert "casual" in prompt

    def test_all_template_ids_are_unique(self):
        templates = list_templates()
        ids = [t["id"] for t in templates]
        assert len(ids) == len(set(ids))
