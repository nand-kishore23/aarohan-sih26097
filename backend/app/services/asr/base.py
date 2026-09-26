"""ASR provider contract."""
from __future__ import annotations

from abc import ABC, abstractmethod


class ASRProviderError(RuntimeError):
    """Base class for clear ASR failures."""


class ASRProviderUnavailableError(ASRProviderError):
    """Raised when a provider is disabled, unavailable, or returns no transcript."""


class ASRProvider(ABC):
    name = "unknown"

    @property
    @abstractmethod
    def configured(self) -> bool:
        """Whether the provider is ready to transcribe audio."""

    @abstractmethod
    def transcribe(self, audio: bytes, filename: str, content_type: str, language: str) -> str:
        """Return a provider-produced transcript, never a guessed transcript."""
