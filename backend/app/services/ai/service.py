"""Grounded conversation orchestration with compact in-memory session state."""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from threading import RLock

from ...models import (
    AIChatRequest,
    AIChatResponse,
    Beneficiary,
    CapabilityObservation,
    CandidatePathway,
    EvidenceRecord,
    LivelihoodProfile,
    Provenance,
    ProvenanceOrigin,
    SkillObservation,
    VerificationStatus,
)
from ...pathway_engine import recommend_pathways
from ...seed_data import QUALIFICATION_CATALOGUE
from ...skill_engine import extract_skills
from .base import AIProvider, AIProviderError
from .gemini import GeminiProvider
from .schemas import GroundedConversationRequest


CAPABILITY_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("mobile_phone_repair", ("phone repair", "mobile repair", "mobile theek", "phone", "mobile", "फोन", "मोबाइल")),
    ("display_replacement", ("display", "screen", "स्क्रीन")),
    ("charging_fault_repair", ("charging", "charge fault", "charging fault", "चार्जिंग")),
    ("soldering", ("soldering", "solder", "सोल्डर")),
    ("tractor_repair", ("tractor", "ट्रैक्टर")),
    ("pump_repair", ("pump", "पंप")),
    ("machine_diagnostics", ("machine", "machine khol", "मशीन")),
    ("electrical_repair", ("electrical", "wiring", "electric", "बिजली")),
)

CAPABILITY_TO_CATALOGUE_SKILLS = {
    "soldering": {"soldering"},
    "tractor_repair": {"tractor_repair", "mechanical_troubleshooting"},
    "pump_repair": {"pump_repair", "mechanical_troubleshooting"},
    "electrical_repair": {"electrical_repair", "wiring"},
}

TRANSFERABLE_SKILLS = {
    "mobile_phone_repair": "device fault diagnosis",
    "display_replacement": "component replacement",
    "charging_fault_repair": "electrical fault diagnosis",
    "soldering": "component soldering",
    "tractor_repair": "mechanical troubleshooting",
    "pump_repair": "equipment maintenance",
    "machine_diagnostics": "machine diagnostics",
    "electrical_repair": "electrical troubleshooting",
}


@dataclass
class ConversationSession:
    profile: LivelihoodProfile
    recent_messages: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)


class SessionStore:
    """Process-local memory for the short prototype conversation window."""

    def __init__(self) -> None:
        self._sessions: dict[str, ConversationSession] = {}
        self._lock = RLock()

    def get_or_create(
        self,
        session_id: str | None,
        language: str,
        profile: LivelihoodProfile | None,
    ) -> tuple[str, ConversationSession]:
        with self._lock:
            resolved_id = session_id or f"session-{uuid.uuid4().hex}"
            if resolved_id not in self._sessions:
                self._sessions[resolved_id] = ConversationSession(
                    profile=profile.model_copy(deep=True) if profile else LivelihoodProfile(language=language)
                )
            return resolved_id, self._sessions[resolved_id]


def _normalized_capabilities(message: str) -> list[CapabilityObservation]:
    lowered = message.casefold()
    observations: list[CapabilityObservation] = []
    for capability, patterns in CAPABILITY_PATTERNS:
        if any(pattern in lowered for pattern in patterns):
            observations.append(
                CapabilityObservation(
                    capability=capability,
                    evidence_text=message,
                    provenance=Provenance(origin=ProvenanceOrigin.DERIVED),
                )
            )
    return observations


def _merge_unique_by_value(existing: list, additions: list, attribute: str) -> list:
    seen = {getattr(item, attribute) for item in existing}
    return [*existing, *(item for item in additions if getattr(item, attribute) not in seen)]


class AIService:
    """Coordinates extraction, deterministic evidence tools, and optional AI explanation."""

    def __init__(self, provider: AIProvider | None = None, sessions: SessionStore | None = None):
        self._provider = provider
        self._sessions = sessions or SessionStore()

    def _provider_for_request(self) -> AIProvider:
        if self._provider is not None:
            return self._provider
        provider_name = os.getenv("AI_PROVIDER", "gemini").strip().lower()
        if provider_name != "gemini":
            raise AIProviderError(f"Unsupported AI_PROVIDER '{provider_name}'. Only 'gemini' is configured.")
        return GeminiProvider()

    def status(self) -> dict[str, object]:
        configured_provider = os.getenv("AI_PROVIDER", "gemini").strip().lower()
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite").strip()
        gemini = GeminiProvider(model=model)
        from ..asr.service import asr_service

        return {
            "ai_provider": configured_provider,
            "ai_configured": configured_provider == "gemini" and gemini.configured,
            "ai_model": model or None,
            "asr_provider": asr_service.provider_name,
            "asr_configured": asr_service.configured,
            "evidence_engine": "available",
            "mode": "ai_grounded" if configured_provider == "gemini" and gemini.configured else "deterministic_fallback",
        }

    def chat(self, request: AIChatRequest) -> AIChatResponse:
        session_id, session = self._sessions.get_or_create(request.session_id, request.language, request.profile)
        profile = session.profile
        profile.language = request.language or profile.language
        profile.raw_statements.append(request.message)
        profile.skills = _merge_unique_by_value(profile.skills, extract_skills(request.message), "normalized_skill")
        new_capabilities = _normalized_capabilities(request.message)
        profile.capabilities = _merge_unique_by_value(profile.capabilities, new_capabilities, "capability")
        profile.tasks_performed = list(dict.fromkeys([*profile.tasks_performed, *(item.capability for item in new_capabilities)]))
        session.recent_messages = [*session.recent_messages[-3:], request.message]

        questions = self._clarification_questions(profile)
        profile.missing_information = self._missing_information(questions)
        profile.conversation_state = "clarifying" if questions else "evidence_review"
        candidates, evidence = self._find_relevant_pathways(profile)
        session.evidence_ids = [item.qualification_id for item in evidence]
        next_step = self._next_step(profile, candidates, questions)
        current_capabilities = [item.capability for item in profile.capabilities]
        transferable_skills = list(
            dict.fromkeys(
                TRANSFERABLE_SKILLS[item]
                for item in current_capabilities
                if item in TRANSFERABLE_SKILLS
            )
        )
        needs_verification = list(profile.missing_information)
        verified_gaps: list[str] = []
        for candidate, evidence_record in zip(candidates, evidence):
            if evidence_record.verification_status == VerificationStatus.VERIFIED:
                verified_gaps.extend(candidate.skill_gaps)
            else:
                needs_verification.extend(candidate.skill_gaps)

        grounded_request = GroundedConversationRequest(
            message=request.message,
            language=profile.language,
            profile=profile,
            evidence=evidence,
            candidate_pathways=candidates,
            questions=questions,
            next_step=next_step,
        )
        warnings: list[str] = []
        provider_name = "deterministic_fallback"
        mode = "deterministic_fallback"
        message = self._deterministic_response(grounded_request)

        try:
            provider = self._provider_for_request()
            if not provider.configured:
                warnings.append("Gemini is not configured; deterministic grounded fallback was used.")
            else:
                message = provider.generate_response(grounded_request)
                provider_name = provider.name
                mode = "ai_grounded"
        except AIProviderError as exc:
            warnings.append(str(exc))

        return AIChatResponse(
            session_id=session_id,
            message=message,
            language=profile.language,
            profile_updates=profile,
            candidate_pathways=candidates,
            evidence=evidence,
            questions=questions,
            next_step=next_step,
            current_capabilities=current_capabilities,
            transferable_skills=transferable_skills,
            already_demonstrated=current_capabilities,
            needs_verification=list(dict.fromkeys(needs_verification)),
            verified_gaps=list(dict.fromkeys(verified_gaps)),
            provenance=[item.provenance for item in profile.capabilities] + [item.provenance for item in evidence],
            provider=provider_name,
            mode=mode,
            warnings=warnings,
        )

    def _clarification_questions(self, profile: LivelihoodProfile) -> list[str]:
        capabilities = {item.capability for item in profile.capabilities}
        hindi = profile.language.lower().startswith("hi")
        if "mobile_phone_repair" in capabilities:
            if not capabilities.intersection({"display_replacement", "charging_fault_repair"}):
                return [
                    "Aap phone mein kis type ka repair karte hain - display/battery, charging, software, ya motherboard level?"
                    if hindi else "Which phone repairs do you do: display/battery, charging, software, or motherboard-level work?"
                ]
            if "soldering" not in capabilities:
                return ["Kya aap soldering bhi karte hain?" if hindi else "Do you also do soldering?"]
        return []

    def _missing_information(self, questions: list[str]) -> list[str]:
        if not questions:
            return []
        return ["soldering experience"] if "solder" in questions[0].casefold() else ["specific repair tasks"]

    def _find_relevant_pathways(
        self, profile: LivelihoodProfile
    ) -> tuple[list[CandidatePathway], list[EvidenceRecord]]:
        capability_names = {item.capability for item in profile.capabilities}
        catalogue_skills = {
            skill
            for capability in capability_names
            for skill in CAPABILITY_TO_CATALOGUE_SKILLS.get(capability, set())
        }
        skill_observations = [
            SkillObservation(
                raw_skill=skill,
                normalized_skill=skill,
                evidence_text="Beneficiary capability normalized from conversation.",
                source_type=ProvenanceOrigin.DERIVED,
                provenance=Provenance(origin=ProvenanceOrigin.DERIVED),
            )
            for skill in sorted(catalogue_skills)
        ]
        beneficiary = Beneficiary(
            id="conversation-session",
            preferred_language=profile.language,
            raw_statement=profile.raw_statements[-1] if profile.raw_statements else "",
            skills=skill_observations,
        )
        candidates = recommend_pathways(beneficiary, QUALIFICATION_CATALOGUE)
        evidence: list[EvidenceRecord] = []
        for candidate in candidates:
            qualification = QUALIFICATION_CATALOGUE[candidate.qualification_id]
            evidence.append(
                EvidenceRecord(
                    qualification_id=qualification.id,
                    qualification_name=qualification.display_name or qualification.name,
                    qp_code=qualification.qp_code,
                    nsqf_level=qualification.nsqf_level,
                    sector=qualification.sector_council,
                    verification_status=qualification.provenance.verification_status,
                    source_name=qualification.provenance.source_name,
                    source_url=qualification.provenance.source_url,
                    relationship="Related to demonstrated capability; formal scope and remaining requirements require human validation.",
                    provenance=qualification.provenance,
                )
            )
        return candidates, evidence

    def _next_step(
        self,
        profile: LivelihoodProfile,
        candidates: list[CandidatePathway],
        questions: list[str],
    ) -> str:
        hindi = profile.language.lower().startswith("hi")
        if questions:
            return "Practical repair tasks ko pehle clear karein, phir pathway matching karein." if hindi else "Clarify practical repair tasks before matching pathways."
        if candidates:
            return "Field ya training-centre representative ke saath related prototype pathway dekhein aur formal eligibility/competency coverage verify karein." if hindi else "Review the related prototype pathway with a field or training-centre representative; verify formal eligibility and competency coverage."
        return "Aur specific practical tasks record karein; current verified prototype catalogue mein supported match nahi mila, isliye field validation zaroori hai." if hindi else "Record more specific practical tasks and seek field validation because the current verified prototype catalogue has no supported match."

    def _deterministic_response(self, request: GroundedConversationRequest) -> str:
        hindi = request.language.lower().startswith("hi")
        capabilities = [item.capability.replace("_", " ") for item in request.profile.capabilities]
        if hindi:
            intro = "Samajh gaya. Aapke bataye hue practical kaam mein " + (", ".join(capabilities) if capabilities else "abhi koi specific capability clear nahi hui") + " shamil hain."
            if request.questions:
                return f"{intro} {request.questions[0]}"
            if request.candidate_pathways:
                names = ", ".join(candidate.pathway_name for candidate in request.candidate_pathways)
                return f"{intro} Available source-backed prototype evidence mein {names} related hai. Yeh formal phone-repair qualification ka claim nahi hai; remaining requirements aur eligibility ko human validation se verify karna hoga. {request.next_step}"
            return f"{intro} Mobile phone repair ke liye current verified prototype catalogue mein koi supported formal pathway evidence nahi mila. Isliye main QP, NSQF level, certificate, ya employment claim nahi kar raha. {request.next_step}"
        intro = "I understand that your demonstrated practical capabilities include " + (", ".join(capabilities) if capabilities else "no specific capability yet") + "."
        if request.questions:
            return f"{intro} {request.questions[0]}"
        if request.candidate_pathways:
            names = ", ".join(candidate.pathway_name for candidate in request.candidate_pathways)
            return f"{intro} The available source-backed prototype evidence identifies {names} as related. This is not a claim of a formal phone-repair qualification; eligibility and remaining requirements need human validation. {request.next_step}"
        return f"{intro} The current verified prototype catalogue has no supported formal pathway evidence for mobile phone repair, so I cannot claim a QP, NSQF level, certificate, or employment outcome. {request.next_step}"


ai_service = AIService()
