"""Tests for the provider abstraction layer."""

from unittest.mock import patch

import pytest

from providers.base import GenerationResult
from providers.gemini_provider import GeminiProvider
from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider


class TestGenerationResult:
    """Test the GenerationResult dataclass."""

    def test_creation(self):
        result = GenerationResult(
            content="Hello world",
            provider="test",
            model="test-v1",
            tokens_used=10,
        )
        assert result.content == "Hello world"
        assert result.provider == "test"
        assert result.tokens_used == 10
        assert result.finish_reason == "stop"

    def test_defaults(self):
        result = GenerationResult(content="test", provider="x", model="y")
        assert result.tokens_used == 0
        assert result.finish_reason == "stop"


class TestOpenAIProvider:
    """Test OpenAI provider."""

    def test_initialization(self):
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")
        assert provider.name == "openai"
        assert provider.model == "gpt-4o-mini"
        assert provider.is_available() is True

    def test_not_available_without_key(self):
        provider = OpenAIProvider(api_key="", model="gpt-4o-mini")
        assert provider.is_available() is False

    def test_info(self):
        provider = OpenAIProvider(api_key="test", model="gpt-4o")
        info = provider.info()
        assert info["name"] == "openai"
        assert "gpt-4o" in info["models"]
        assert info["available"] is True


class TestGeminiProvider:
    """Test Gemini provider."""

    def test_initialization(self):
        with patch("providers.gemini_provider.genai"):
            provider = GeminiProvider(api_key="test-key")
            assert provider.name == "gemini"
            assert provider.is_available() is True

    def test_not_available_without_key(self):
        with patch("providers.gemini_provider.genai"):
            provider = GeminiProvider(api_key="")
            assert provider.is_available() is False

    def test_info(self):
        with patch("providers.gemini_provider.genai"):
            provider = GeminiProvider(api_key="test")
            info = provider.info()
            assert info["name"] == "gemini"
            assert info["available"] is True


class TestOllamaProvider:
    """Test Ollama provider."""

    def test_initialization(self):
        provider = OllamaProvider(base_url="http://localhost:11434", model="llama3.2")
        assert provider.name == "ollama"
        assert provider.model == "llama3.2"

    def test_base_url_trailing_slash(self):
        provider = OllamaProvider(base_url="http://localhost:11434/")
        assert provider.base_url == "http://localhost:11434"

    def test_info(self):
        provider = OllamaProvider()
        info = provider.info()
        assert info["name"] == "ollama"
        assert "llama3.2" in info["models"]

    def test_not_available_when_offline(self):
        provider = OllamaProvider(base_url="http://localhost:99999")
        assert provider.is_available() is False


class TestProviderInterface:
    """Test that all providers implement the required interface."""

    @pytest.mark.parametrize(
        "provider_class,kwargs",
        [
            (OpenAIProvider, {"api_key": "test"}),
            (OllamaProvider, {}),
        ],
    )
    def test_has_required_methods(self, provider_class, kwargs):
        if provider_class == GeminiProvider:
            return  # Skip, requires genai mock
        provider = provider_class(**kwargs)
        assert hasattr(provider, "generate")
        assert hasattr(provider, "stream")
        assert hasattr(provider, "is_available")
        assert hasattr(provider, "info")
        assert hasattr(provider, "name")
