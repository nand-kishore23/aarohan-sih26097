"""Official Google GenAI SDK adapter, imported only when it is actually used."""
from __future__ import annotations

import json
import os

from .base import AIProvider, AIProviderConfigurationError, AIProviderUnavailableError
from .prompts import SYSTEM_PROMPT, UNDERSTANDING_SYSTEM_PROMPT
from ..latency import timed
from .schemas import (
    GeminiUnderstanding,
    GroundedConversationRequest,
    UnderstandingRequest,
    validate_gemini_understanding,
)


class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY", "").strip()
        # Gemini 3.5 Flash-Lite is configurable and currently documented with a free tier.
        env_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
        if env_model == "gemini-2.5-flash-lite":
            env_model = "gemini-3.5-flash-lite"
        self.model = model if model is not None else env_model

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.model)

    def understand(self, request: UnderstandingRequest) -> GeminiUnderstanding:
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

        contents = {
            "beneficiary_message": request.message,
            "requested_language": request.language,
            "recent_beneficiary_messages": request.recent_messages[-4:],
        }
        schema_dict = GeminiUnderstanding.model_json_schema()
        schema_dict.pop("additionalProperties", None)

        try:
            client = genai.Client(api_key=self.api_key)
            with timed("gemini", "understanding", model=self.model):
                response = client.models.generate_content(
                    model=self.model,
                    contents=json.dumps(contents, ensure_ascii=False),
                    config=types.GenerateContentConfig(
                        system_instruction=UNDERSTANDING_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=schema_dict,
                        temperature=0.0,
                    ),
                )
            with timed("ai_chat", "structured_output_parse"):
                parsed = getattr(response, "parsed", None)
                raw_result = parsed if parsed is not None else json.loads(response.text or "")
                return validate_gemini_understanding(raw_result)
        except (ValueError, TypeError) as exc:
            raise AIProviderUnavailableError("Gemini returned invalid structured understanding.") from exc
        except Exception as exc:  # Provider exceptions vary by SDK version and HTTP status.
            raise AIProviderUnavailableError(
                f"Gemini understanding request failed for configured model '{self.model}': {exc}"
            ) from exc

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
            "accepted_capabilities": request.accepted_capabilities,
            "unresolved_capabilities": request.unresolved_capabilities,
            "missing_information": request.missing_information,
            "verified_evidence": [item.model_dump(mode="json") for item in request.evidence],
            "candidate_pathways": [item.model_dump(mode="json") for item in request.candidate_pathways],
            "clarification_questions": request.questions,
            "deterministic_next_step": request.next_step,
        }

        try:
            client = genai.Client(api_key=self.api_key)
            with timed("gemini", "grounded_explanation", model=self.model):
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

        with timed("ai_chat", "grounded_response_parse"):
            text = getattr(response, "text", None)
            if not text or not text.strip():
                raise AIProviderUnavailableError(
                    f"Gemini returned no usable text for configured model '{self.model}'."
                )
            return text.strip()
