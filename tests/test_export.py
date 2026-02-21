"""Tests for content export functionality."""

import json

from export import export_content, strip_markdown


class TestExportContent:
    """Test export format conversion."""

    def test_markdown_passthrough(self):
        content = "# Title\n\nSome **bold** text"
        result = export_content(content, "markdown")
        assert result == content

    def test_plain_text_strips_markdown(self):
        content = "# Title\n\nSome **bold** text with [link](http://example.com)"
        result = export_content(content, "plain")
        assert "#" not in result
        assert "**" not in result
        assert "http://example.com" not in result
        assert "Title" in result
        assert "bold" in result
        assert "link" in result

    def test_json_format(self):
        content = "Hello world"
        result = export_content(content, "json")
        parsed = json.loads(result)
        assert parsed["content"] == "Hello world"
        assert parsed["format"] == "markdown"

    def test_default_is_markdown(self):
        content = "# Test"
        result = export_content(content)
        assert result == content


class TestStripMarkdown:
    """Test markdown stripping."""

    def test_strips_headers(self):
        assert "Title" in strip_markdown("## Title")
        assert "#" not in strip_markdown("## Title")

    def test_strips_bold_italic(self):
        result = strip_markdown("**bold** and *italic*")
        assert "bold" in result
        assert "italic" in result
        assert "*" not in result

    def test_strips_code(self):
        result = strip_markdown("Use `print()` function")
        assert "print()" in result
        assert "`" not in result

    def test_strips_links(self):
        result = strip_markdown("[Click here](http://example.com)")
        assert "Click here" in result
        assert "http" not in result

    def test_strips_list_markers(self):
        result = strip_markdown("- Item 1\n- Item 2")
        assert "Item 1" in result
        assert result.startswith("Item")

    def test_collapses_multiple_newlines(self):
        result = strip_markdown("A\n\n\n\nB")
        assert "\n\n\n" not in result

    def test_empty_string(self):
        assert strip_markdown("") == ""
