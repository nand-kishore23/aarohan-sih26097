"""ASR orchestration with an honest browser-transcript fallback."""
from __future__ import annotations

import os

from .ai4bharat import AI4BharatASRProvider
from .base import ASRProvider, ASRProviderUnavailableError
from .fallback import BrowserFallbackASRProvider


class ASRService:
    def __init__(self, provider: ASRProvider | None = None):
        self._provider = provider

    def _provider_for_request(self) -> ASRProvider:
        if self._provider is not None:
            return self._provider
        provider_name = os.getenv("ASR_PROVIDER", "browser_fallback").strip().lower()
        if provider_name == "ai4bharat":
            return AI4BharatASRProvider()
        if provider_name == "browser_fallback":
            return BrowserFallbackASRProvider()
        raise ASRProviderUnavailableError(
            f"Unsupported ASR_PROVIDER '{provider_name}'. Use 'ai4bharat' or 'browser_fallback'."
        )

    @property
    def provider_name(self) -> str:
        try:
            return self._provider_for_request().name
        except ASRProviderUnavailableError:
            return "unavailable"

    @property
    def configured(self) -> bool:
        try:
            return self._provider_for_request().configured
        except ASRProviderUnavailableError:
            return False

    def transcribe(
        self,
        audio: bytes,
        filename: str,
        content_type: str,
        language: str,
        fallback_text: str | None = None,
    ) -> dict[str, str]:
        provider = self._provider_for_request()
        if provider.name == "browser_fallback":
            if fallback_text and fallback_text.strip():
                return {
                    "text": fallback_text.strip(),
                    "language": language,
                    "provider": provider.name,
                    "status": "fallback",
                }
            raise ASRProviderUnavailableError(
                "No server ASR is configured and no browser-produced fallback_text was supplied."
            )
        text = provider.transcribe(audio, filename, content_type, language)
        return {"text": text, "language": language, "provider": provider.name, "status": "success"}


asr_service = ASRService()
