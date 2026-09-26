"""Official Google GenAI SDK adapter, imported only when it is actually used."""
from __future__ import annotations

import json
import os

from .base import AIProvider, AIProviderConfigurationError, AIProviderUnavailableError
from .prompts import SYSTEM_PROMPT
from .schemas import GroundedConversationRequest


class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY", "").strip()
        # Gemini 2.5 Flash-Lite is configurable and currently documented with a free tier.
        self.model = model if model is not None else os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite").strip()

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.model)

    def generate_response(self, request: GroundedConversationRequest) -> str:
        if not self.api_key:
            raise AIProviderConfigurationError("GEMINI_API_KEY is not configured.")
        if not self.model:
            raise AIProviderConfigurationError("GEMINI_MODEL is not configured.")

        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise AIProviderConfigurationError(
                "google-genai is not installed; install backend requirements before enabling Gemini."
            ) from exc

        grounding = {
            "language": request.language,
            "beneficiary_message": request.message,
            "profile": request.profile.model_dump(mode="json"),
            "verified_evidence": [item.model_dump(mode="json") for item in request.evidence],
            "candidate_pathways": [item.model_dump(mode="json") for item in request.candidate_pathways],
            "clarification_questions": request.questions,
            "deterministic_next_step": request.next_step,
        }

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=json.dumps(grounding, ensure_ascii=False),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                ),
            )
        except Exception as exc:  # Provider exceptions vary by SDK version and HTTP status.
            raise AIProviderUnavailableError(
                f"Gemini request failed for configured model '{self.model}': {exc}"
            ) from exc

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise AIProviderUnavailableError(
                f"Gemini returned no usable text for configured model '{self.model}'."
            )
        return text.strip()
