"""Optional AI4Bharat IndicConformer-compatible endpoint adapter.

The model is intentionally not bundled into the Render service. Deploy it separately or locally,
then configure a private endpoint that accepts multipart audio and returns {"text": "..."}.
"""
from __future__ import annotations

import os

import httpx

from .base import ASRProvider, ASRProviderUnavailableError


class AI4BharatASRProvider(ASRProvider):
    name = "ai4bharat"

    def __init__(self, endpoint: str | None = None, model: str | None = None):
        self.endpoint = endpoint if endpoint is not None else os.getenv("AI4BHARAT_ENDPOINT", "").strip()
        self.model = model if model is not None else os.getenv("AI4BHARAT_MODEL", "").strip()

    @property
    def configured(self) -> bool:
        return bool(self.endpoint and self.model)

    def transcribe(self, audio: bytes, filename: str, content_type: str, language: str) -> str:
        if not self.configured:
            raise ASRProviderUnavailableError(
                "AI4Bharat ASR is not configured. Set AI4BHARAT_ENDPOINT and AI4BHARAT_MODEL, or use browser fallback."
            )
        try:
            response = httpx.post(
                self.endpoint,
                files={"audio": (filename, audio, content_type)},
                data={"model": self.model, "language": language},
                timeout=45.0,
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ASRProviderUnavailableError(f"AI4Bharat ASR endpoint failed: {exc}") from exc

        text = payload.get("text") if isinstance(payload, dict) else None
        if not isinstance(text, str) or not text.strip():
            raise ASRProviderUnavailableError("AI4Bharat ASR endpoint returned no transcript.")
        return text.strip()
