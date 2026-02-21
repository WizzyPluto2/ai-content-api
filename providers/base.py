"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class GenerationResult:
    """Result from an LLM generation call."""

    content: str
    provider: str
    model: str
    tokens_used: int = 0
    finish_reason: str = "stop"


class BaseProvider(ABC):
    """Abstract interface that all LLM providers implement."""

    name: str = ""
    models: list[str] = []

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> GenerationResult:
        """Generate content (non-streaming)."""
        ...

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncIterator[str]:
        """Generate content as a stream of text chunks."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is configured and reachable."""
        ...

    def info(self) -> dict:
        """Return provider metadata."""
        return {
            "name": self.name,
            "models": self.models,
            "available": self.is_available(),
        }
