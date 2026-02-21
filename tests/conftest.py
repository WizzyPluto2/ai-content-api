"""Shared test fixtures."""

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Use temp database for tests
os.environ["DATABASE_URL"] = "sqlite:///test_data/test.db"
os.environ["OPENAI_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = ""
os.environ["DEFAULT_PROVIDER"] = "ollama"


@pytest.fixture(autouse=True)
def clean_test_db(tmp_path):
    """Use a fresh temp database for each test."""
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    # Re-patch the module-level DB_PATH
    import database.connection as conn

    conn.DB_PATH = db_path
    yield
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def mock_provider():
    """Returns a mock LLM provider."""
    from providers.base import BaseProvider, GenerationResult

    provider = MagicMock(spec=BaseProvider)
    provider.name = "mock"
    provider.model = "mock-v1"
    provider.models = ["mock-v1"]
    provider.is_available.return_value = True
    provider.info.return_value = {
        "name": "mock",
        "models": ["mock-v1"],
        "available": True,
    }
    provider.generate = AsyncMock(
        return_value=GenerationResult(
            content="Generated test content about the requested topic.",
            provider="mock",
            model="mock-v1",
            tokens_used=42,
            finish_reason="stop",
        )
    )
    return provider


@pytest.fixture
def sample_variables():
    """Sample template variables for testing."""
    return {
        "topic": "AI testing best practices",
        "tone": "professional",
        "word_count": "500",
        "keywords": "testing, pytest, automation",
    }
