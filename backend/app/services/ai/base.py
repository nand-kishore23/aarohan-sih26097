"""Provider contract for conversational reasoning."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import GroundedConversationRequest


class AIProviderError(RuntimeError):
    """Base class for provider errors that must be disclosed to callers."""


class AIProviderConfigurationError(AIProviderError):
    """Raised when a configured provider cannot be used safely."""


class AIProviderUnavailableError(AIProviderError):
    """Raised for transient provider/model/API failures."""


class AIProvider(ABC):
    name = "unknown"

    @property
    @abstractmethod
    def configured(self) -> bool:
        """Whether the provider has the minimum safe configuration."""

    @abstractmethod
    def generate_response(self, request: GroundedConversationRequest) -> str:
        """Generate explanation only from structured grounding provided by the app."""
