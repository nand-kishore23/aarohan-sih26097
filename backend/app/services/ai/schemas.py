"""Internal schemas shared between the orchestration service and AI providers."""
from __future__ import annotations

from dataclasses import dataclass

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
