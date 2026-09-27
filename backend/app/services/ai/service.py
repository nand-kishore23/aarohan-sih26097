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
    ReportedStatement,
    SkillObservation,
    VerificationStatus,
)
from ...pathway_engine import recommend_pathways
from ...seed_data import QUALIFICATION_CATALOGUE
from ...skill_engine import extract_skills
from ..latency import timed
from .base import AIProvider, AIProviderError
from .gemini import GeminiProvider
from .schemas import (
    GeminiUnderstanding,
    GroundedConversationRequest,
    UnderstandingRequest,
    validate_gemini_understanding,
)


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

# Only these application-owned capability IDs can reach deterministic matching.
CAPABILITY_ALLOWLIST = frozenset(
    {
        "mobile_phone_repair",
        "display_replacement",
        "charging_fault_repair",
        "soldering",
        "tractor_repair",
        "pump_repair",
        "machine_diagnostics",
        "electrical_repair",
        "appliance_repair",
        "dairy_processing",
        "milk_testing",
        "pasteurization",
    }
)

CAPABILITY_TO_CATALOGUE_SKILLS = {
    "soldering": {"soldering"},
    "tractor_repair": {"tractor_repair", "mechanical_troubleshooting"},
    "pump_repair": {"pump_repair", "mechanical_troubleshooting"},
    "electrical_repair": {"electrical_repair", "wiring"},
    "appliance_repair": {"appliance_repair"},
    "dairy_processing": {"dairy_processing"},
    "milk_testing": {"milk_testing"},
    "pasteurization": {"pasteurization"},
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


def _fallback_capabilities(message: str) -> list[CapabilityObservation]:
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


def _merge_capabilities(
    existing: list[CapabilityObservation],
    additions: list[CapabilityObservation],
) -> list[CapabilityObservation]:
    seen = {(item.capability, item.normalized_from) for item in existing}
    return [
        *existing,
        *(
            item
            for item in additions
            if (item.capability, item.normalized_from) not in seen
        ),
    ]


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
        gemini = GeminiProvider()
        from ..asr.service import asr_service

        return {
            "ai_provider": configured_provider,
            "ai_configured": configured_provider == "gemini" and gemini.configured,
            "ai_model": gemini.model or None,
            "asr_provider": asr_service.provider_name,
            "asr_configured": asr_service.configured,
            "evidence_engine": "available",
            "mode": "ai_grounded" if configured_provider == "gemini" and gemini.configured else "deterministic_fallback",
        }

    def chat(self, request: AIChatRequest) -> AIChatResponse:
        with timed("ai_chat", "profile_prepare"):
            session_id, session = self._sessions.get_or_create(request.session_id, request.language, request.profile)
            profile = session.profile
            profile.language = request.language or profile.language
            profile.raw_statements.append(request.message)
            profile.self_reported_statements.append(ReportedStatement(text=request.message))
            session.recent_messages = [*session.recent_messages[-3:], request.message]

        warnings: list[str] = []
        provider_name = "deterministic_fallback"
        mode = "deterministic_fallback"
        provider: AIProvider | None = None
        understanding: GeminiUnderstanding | None = None
        try:
            with timed("ai_chat", "provider_prepare"):
                provider = self._provider_for_request()
            if provider.configured:
                with timed("ai_chat", "understanding_dispatch"):
                    understanding = validate_gemini_understanding(
                        provider.understand(
                            UnderstandingRequest(
                                message=request.message,
                                language=profile.language,
                                recent_messages=session.recent_messages,
                            )
                        )
                    )
            else:
                warnings.append("Gemini is not configured; deterministic grounded fallback was used.")
        except ValueError:
            # Do not echo rejected model payloads into beneficiary-facing responses or logs.
            warnings.append("Gemini structured understanding failed validation; deterministic fallback was used.")
        except AIProviderError:
            warnings.append("Gemini structured understanding was unavailable; deterministic fallback was used.")

        if understanding is not None:
            with timed("ai_chat", "understanding_apply"):
                new_capabilities = self._apply_understanding(profile, understanding, request.message)
                derived_skills = self._skills_for_capabilities(new_capabilities)
                profile.skills = _merge_unique_by_value(profile.skills, derived_skills, "normalized_skill")
            provider_name = provider.name if provider else provider_name
            mode = "ai_grounded"
        else:
            # Existing deterministic extraction is retained only for Gemini-disabled/unavailable mode.
            with timed("ai_chat", "deterministic_skill_extraction"):
                fallback_skills = extract_skills(request.message)
                profile.skills = _merge_unique_by_value(profile.skills, fallback_skills, "normalized_skill")
                new_capabilities = _fallback_capabilities(request.message)
                profile.capabilities = _merge_capabilities(profile.capabilities, new_capabilities)
                profile.tasks_performed = list(
                    dict.fromkeys([*profile.tasks_performed, *(item.capability for item in new_capabilities)])
                )

        with timed("ai_chat", "interview_state"):
            deterministic_questions = self._clarification_questions(profile)
            questions = self._questions_from_understanding(understanding, deterministic_questions)
            profile.missing_information = list(
                dict.fromkeys(
                    [
                        *(understanding.missing_information if understanding else []),
                        *self._missing_information(questions),
                    ]
                )
            )
            profile.conversation_state = "clarifying" if questions else "evidence_review"

        # Gate pathway generation: do not run the deterministic engine while
        # there are outstanding questions.  This forces multi-turn interview
        # behaviour — pathways are only generated once the profile is
        # sufficiently understood.
        with timed("ai_chat", "evidence_gate"):
            if questions:
                candidates: list[CandidatePathway] = []
                evidence: list[EvidenceRecord] = []
            else:
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

        with timed("ai_chat", "grounded_response_build"):
            grounded_request = GroundedConversationRequest(
                message=request.message,
                language=profile.language,
                profile=profile,
                evidence=evidence,
                candidate_pathways=candidates,
                questions=questions,
                next_step=next_step,
                accepted_capabilities=[
                    item.capability
                    for item in profile.capabilities
                    if item.capability != "UNRESOLVED_SKILL"
                ],
                unresolved_capabilities=[
                    item.normalized_from or item.evidence_text
                    for item in profile.capabilities
                    if item.capability == "UNRESOLVED_SKILL"
                ],
                missing_information=profile.missing_information,
            )
            message = self._deterministic_response(grounded_request)

        try:
            # Clarifying turns are deliberately deterministic and compact. The structured
            # understanding provider supplies the one question; grounded explanation is
            # reserved for the completed interview so internal evidence language cannot
            # leak into the conversation.
            if not questions and provider is not None and provider.configured:
                message = provider.generate_response(grounded_request)
                provider_name = provider.name
                mode = "ai_grounded"
        except AIProviderError:
            warnings.append("Gemini grounded explanation was unavailable; deterministic response was used.")

        with timed("ai_chat", "response_build"):
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

    def _apply_understanding(
        self,
        profile: LivelihoodProfile,
        understanding: GeminiUnderstanding,
        raw_statement: str,
    ) -> list[CapabilityObservation]:
        observations: list[CapabilityObservation] = []
        for capability in understanding.capabilities:
            if capability in CAPABILITY_ALLOWLIST:
                observations.append(
                    CapabilityObservation(
                        capability=capability,
                        evidence_text=raw_statement,
                        provenance=Provenance(origin=ProvenanceOrigin.DERIVED),
                    )
                )
            else:
                observations.append(
                    CapabilityObservation(
                        capability="UNRESOLVED_SKILL",
                        normalized_from=capability,
                        evidence_text=raw_statement,
                        provenance=Provenance(origin=ProvenanceOrigin.DERIVED),
                    )
                )
        profile.capabilities = _merge_capabilities(profile.capabilities, observations)
        profile.tasks_performed = list(dict.fromkeys([*profile.tasks_performed, *understanding.reported_tasks]))
        profile.interests = list(dict.fromkeys([*profile.interests, *understanding.interests]))
        if understanding.current_work_description:
            profile.current_livelihood = understanding.current_work_description
        if understanding.experience_duration:
            profile.experience_duration = understanding.experience_duration
        if understanding.learning_source:
            profile.informal_experience = list(
                dict.fromkeys([*profile.informal_experience, understanding.learning_source])
            )
        if understanding.work_preference:
            profile.work_preference = understanding.work_preference
        return observations

    def _skills_for_capabilities(
        self, observations: list[CapabilityObservation]
    ) -> list[SkillObservation]:
        skills = {
            skill
            for observation in observations
            for skill in CAPABILITY_TO_CATALOGUE_SKILLS.get(observation.capability, set())
        }
        return [
            SkillObservation(
                raw_skill=skill,
                normalized_skill=skill,
                evidence_text="AAROHAN mapped an allowlisted Gemini-derived capability to a canonical skill.",
                source_type=ProvenanceOrigin.DERIVED,
                provenance=Provenance(origin=ProvenanceOrigin.DERIVED),
            )
            for skill in sorted(skills)
        ]

    def _questions_from_understanding(
        self,
        understanding: GeminiUnderstanding | None,
        deterministic_questions: list[str],
    ) -> list[str]:
        if understanding and understanding.clarification_question:
            return [understanding.clarification_question]
        return deterministic_questions

    def _clarification_questions(self, profile: LivelihoodProfile) -> list[str]:
        capabilities = {item.capability for item in profile.capabilities}
        hindi = profile.language.lower().startswith("hi")

        # Phone-repair sub-type questions (existing)
        if "mobile_phone_repair" in capabilities:
            if not capabilities.intersection({"display_replacement", "charging_fault_repair"}):
                return [
                    "Aap phone mein kis type ka repair karte hain - display/battery, charging, software, ya motherboard level?"
                    if hindi else "Which phone repairs do you do: display/battery, charging, software, or motherboard-level work?"
                ]
            if "soldering" not in capabilities:
                return ["Kya aap soldering bhi karte hain?" if hindi else "Do you also do soldering?"]

        # Generic sparse-profile questions: if we have capabilities but the
        # profile is missing basic context that would improve pathway matching.
        # Deterministic fallback relies on turn counts since it can't populate fields.
        resolved = {c for c in capabilities if c != "UNRESOLVED_SKILL"}
        if resolved:
            if len(profile.raw_statements) == 1 and not profile.experience_duration:
                return [
                    "Aap yeh kaam kitne samay se kar rahe hain?"
                    if hindi else "How long have you been doing this work?"
                ]
            if len(profile.raw_statements) == 2 and not profile.work_preference:
                return [
                    "Aap naukri dhundh rahe hain ya apna kaam shuru karna chahte hain?"
                    if hindi else "Are you looking for employment or self-employment?"
                ]
        return []

    def _missing_information(self, questions: list[str]) -> list[str]:
        if not questions:
            return []
        q = questions[0].casefold()
        if "solder" in q:
            return ["soldering experience"]
        if "samay" in q or "long" in q:
            return ["experience duration"]
        if "naukri" in q or "employment" in q:
            return ["work preference"]
        return ["specific repair tasks"]

    def _find_relevant_pathways(
        self, profile: LivelihoodProfile
    ) -> tuple[list[CandidatePathway], list[EvidenceRecord]]:
        with timed("ai_chat", "evidence_prepare"):
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
        with timed("ai_chat", "pathway_evaluation"):
            candidates = recommend_pathways(beneficiary, QUALIFICATION_CATALOGUE)
        with timed("ai_chat", "qualification_evaluation"):
            evidence = [
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
                for candidate in candidates
                for qualification in [QUALIFICATION_CATALOGUE[candidate.qualification_id]]
            ]
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
        if hindi:
            if request.questions:
                return f"Samajh gaya. {request.questions[0]}"
            if request.candidate_pathways:
                return "Dhanyavaad. Aapki jaankari ke aadhaar par neeche kuch candidate pathways diye gaye hain."
            return "Dhanyavaad. Aapki jaankari record kar li gayi hai. Neeche saaransh dekhein."
        if request.questions:
            return f"I understand. {request.questions[0]}"
        if request.candidate_pathways:
            return "Thank you. Based on what you shared, some candidate pathways are shown below."
        return "Thank you. Your details have been recorded. See the summary below."


ai_service = AIService()
