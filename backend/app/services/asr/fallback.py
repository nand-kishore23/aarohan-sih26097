"""Browser transcript hand-off; this provider never fabricates a transcription."""
from __future__ import annotations

from .base import ASRProvider, ASRProviderUnavailableError


class BrowserFallbackASRProvider(ASRProvider):
    name = "browser_fallback"

    @property
    def configured(self) -> bool:
        # The existing browser SpeechRecognition implementation is client-side.
        return True

    def transcribe(self, audio: bytes, filename: str, content_type: str, language: str) -> str:
        raise ASRProviderUnavailableError(
            "Server-side browser fallback cannot transcribe audio. Send the browser-produced transcript as fallback_text."
        )
