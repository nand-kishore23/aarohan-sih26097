"""Internal schemas shared between the orchestration service and AI providers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ...models import CandidatePathway, EvidenceRecord, LivelihoodProfile


@dataclass(frozen=True)
class GroundedConversationRequest:
    message: str
    language: str
    profile: LivelihoodProfile
    evidence: list[EvidenceRecord]
    candidate_pathways: list[CandidatePathway]
    questions: list[str]
    next_step: str
    accepted_capabilities: list[str]
    unresolved_capabilities: list[str]
    missing_information: list[str]


@dataclass(frozen=True)
class UnderstandingRequest:
    """Only beneficiary conversation context, never qualification evidence."""

    message: str
    language: str
    recent_messages: list[str]


class GeminiUnderstanding(BaseModel):
    """Narrow, conversationally-derived output returned by Gemini.

    Capability names are validated again by AAROHAN before use. This schema deliberately
    has no qualification, evidence, opportunity, or employment fields.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    language: str = "hi"
    reported_tasks: list[str] = Field(default_factory=list, max_length=12)
    capabilities: list[str] = Field(default_factory=list, max_length=12)
    interests: list[str] = Field(default_factory=list, max_length=8)
    current_work_description: str | None = Field(default=None, max_length=400)
    missing_information: list[str] = Field(default_factory=list, max_length=8)
    clarification_question: str | None = Field(default=None, max_length=300)


def validate_gemini_understanding(value: GeminiUnderstanding | dict[str, Any]) -> GeminiUnderstanding:
    """Re-validate provider output even when an SDK has already parsed it."""

    return GeminiUnderstanding.model_validate(value)
