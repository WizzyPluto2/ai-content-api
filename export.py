"""Export generated content in different formats."""

import json
import re


def export_content(content: str, fmt: str = "markdown") -> str:
    """Export content in the specified format."""
    if fmt == "plain":
        return strip_markdown(content)
    elif fmt == "json":
        return json.dumps({"content": content, "format": "markdown"}, indent=2, ensure_ascii=False)
    return content


def strip_markdown(text: str) -> str:
    """Remove common markdown formatting."""
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
