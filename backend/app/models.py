"""AAROHAN Data Models — Pydantic schemas with provenance support."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Provenance ────────────────────────────────────────────────────────
class ProvenanceOrigin(str, Enum):
    SOURCE_BACKED = "SOURCE_BACKED"
    SELF_REPORTED = "SELF_REPORTED"
    DERIVED = "DERIVED"
    SYNTHETIC = "SYNTHETIC"
    MISSING = "MISSING"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    REQUIRES_VERIFICATION = "REQUIRES_VERIFICATION"
    UNVERIFIED = "UNVERIFIED"
    MISSING = "MISSING"


class Provenance(BaseModel):
    origin: ProvenanceOrigin
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    retrieved_at: Optional[str] = None


# ── Skills ────────────────────────────────────────────────────────────
class SkillObservation(BaseModel):
    raw_skill: str
    normalized_skill: str
    evidence_text: str
    source_type: ProvenanceOrigin = ProvenanceOrigin.SELF_REPORTED
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.SELF_REPORTED)
    )


# ── Qualifications ───────────────────────────────────────────────────
class Competency(BaseModel):
    code: str
    name: str
    description: str = ""
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(
            origin=ProvenanceOrigin.SOURCE_BACKED,
            verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        )
    )


class QualificationNOS(BaseModel):
    code: str
    name: str
    core_or_elective: str = "core"  # "core" | "elective"
    nsqf_level: int = 4
    competencies: list[Competency] = []
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(
            origin=ProvenanceOrigin.SOURCE_BACKED,
            verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        )
    )


class QualificationTraining(BaseModel):
    theory_hours: Optional[int] = None
    practical_hours: Optional[int] = None
    ojt_hours: Optional[int] = None
    total_hours: Optional[int] = None


class Qualification(BaseModel):
    id: str
    qp_code: str
    name: str
    display_name: str = ""
    version: Optional[str] = None
    status: str = "PROTOTYPE"
    nsqf_level: int = 4
    sector_council: str = ""
    occupational_area: str = ""
    nos: list[QualificationNOS] = []
    eligibility: list[str] = []
    training: QualificationTraining = Field(default_factory=QualificationTraining)
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(
            origin=ProvenanceOrigin.SOURCE_BACKED,
            verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        )
    )
    # Skills required (simplified for prototype matching)
    required_skills: list[str] = []


# ── Beneficiary ──────────────────────────────────────────────────────
class Beneficiary(BaseModel):
    id: str
    name: str = "Demo Beneficiary"
    age_group: str = ""
    education: str = ""
    district: str = ""
    preferred_language: str = "Hindi"
    current_livelihood: str = ""
    work_experience: str = ""
    employment_preference: str = "employment"
    mobility_radius_km: int = 50
    physical_constraint: Optional[str] = None
    data_origin: ProvenanceOrigin = ProvenanceOrigin.SYNTHETIC
    skills: list[SkillObservation] = []
    interests: list[str] = []
    pathway_interest: Optional[str] = None
    raw_statement: str = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


# ── Candidate Pathways ───────────────────────────────────────────────
class CandidatePathway(BaseModel):
    id: str
    pathway_name: str
    qp_code: str
    nsqf_level: int = 4
    sector: str = ""
    supporting_skills: list[str] = []
    skill_gaps: list[str] = []
    access_constraints: list[str] = []
    evidence_status: str = "PARTIALLY_VERIFIED"
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(
            origin=ProvenanceOrigin.DERIVED,
            verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        )
    )
    why_this: list[str] = []
    why_not: list[str] = []
    qualification_id: str = ""


# ── Interview ────────────────────────────────────────────────────────
class InterviewRequest(BaseModel):
    text: str
    language: str = "hi"
    demo_mode: bool = True


class InterviewResponse(BaseModel):
    interview_id: str
    beneficiary: Beneficiary
    skills: list[SkillObservation]
    message: str = "Interview processed successfully"


# ── Pathway Recommendation ──────────────────────────────────────────
class PathwayRecommendRequest(BaseModel):
    beneficiary_id: str


class PathwayRecommendResponse(BaseModel):
    beneficiary_id: str
    pathways: list[CandidatePathway]
    count: int
    message: str = ""
    disclaimer: str = "AI-assisted analysis — Human review required"


# ── Decision ─────────────────────────────────────────────────────────
class DecisionType(str, Enum):
    INTERESTED = "interested"
    NEED_MORE_INFO = "need_more_info"
    NOT_SUITABLE = "not_suitable"


class PathwayDecisionRequest(BaseModel):
    decision: DecisionType
    notes: str = ""


class PathwayDecisionResponse(BaseModel):
    pathway_id: str
    decision: DecisionType
    recorded_at: str
    message: str = "Decision recorded successfully"
# -- Community Intelligence ------------------------------------------

class TrainingCapacity(BaseModel):
    id: str
    district: str
    pathway_id: str
    qualification_id: str
    provider_name: str
    available_seats: int
    delivery_mode: str = "in_person"
    period_start: str
    period_end: str
    data_origin: ProvenanceOrigin = ProvenanceOrigin.SYNTHETIC
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.SYNTHETIC)
    )

class OpportunitySignal(BaseModel):
    id: str
    pathway_id: str
    district: str
    signal_type: str
    signal_value: str
    source_name: str
    source_reference: str
    published_date: str
    retrieved_at: str
    coverage: str
    status: str = "ACTIVE"
    data_origin: ProvenanceOrigin = ProvenanceOrigin.SYNTHETIC
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.SYNTHETIC)
    )

class PathwayAggregation(BaseModel):
    pathway_id: str
    qualification_id: str
    pathway_name: str
    observed_interest_count: int
    training_capacity: int
    interest_capacity_gap: int
    mismatch_status: str
    opportunity_evidence_status: str
    data_origin: ProvenanceOrigin = ProvenanceOrigin.DERIVED
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.DERIVED)
    )

class CommunitySummary(BaseModel):
    district: str
    data_period: str
    beneficiaries_represented: int
    pathways: list[PathwayAggregation]
    data_origin: ProvenanceOrigin = ProvenanceOrigin.DERIVED
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.DERIVED)
    )

class EvidenceBrief(BaseModel):
    district: str
    data_period: str
    beneficiaries_represented: int
    observed_interest_summary: str
    training_capacity_summary: str
    potential_mismatch_summary: str
    opportunity_evidence_status: str
    evidence_gaps: list[str]
    suggested_next_validation: list[str]
    disclaimer_1: str = "AI-assisted analytical brief — human review required"
    disclaimer_2: str = "Prototype demonstration using synthetic data."


# ── Conversational AI ────────────────────────────────────────────────
class CapabilityObservation(BaseModel):
    """A normalized capability inferred from a beneficiary statement.

    This remains derived conversational input, not qualification evidence.
    """

    capability: str
    evidence_text: str
    provenance: Provenance = Field(
        default_factory=lambda: Provenance(origin=ProvenanceOrigin.DERIVED)
    )


class LivelihoodProfile(BaseModel):
    """Session-scoped profile assembled from beneficiary conversation."""

    language: str = "hi"
    raw_statements: list[str] = []
    current_livelihood: Optional[str] = None
    informal_experience: list[str] = []
    skills: list[SkillObservation] = []
    capabilities: list[CapabilityObservation] = []
    tools_used: list[str] = []
    tasks_performed: list[str] = []
    experience_duration: Optional[str] = None
    education: Optional[str] = None
    certifications: list[str] = []
    interests: list[str] = []
    work_preference: Optional[str] = None
    mobility: Optional[str] = None
    physical_constraints: list[str] = []
    location: Optional[str] = None
    enterprise_interest: Optional[bool] = None
    wage_interest: Optional[bool] = None
    self_employment_interest: Optional[bool] = None
    missing_information: list[str] = []
    conversation_state: str = "collecting"


class EvidenceRecord(BaseModel):
    """Structured evidence passed to the conversational reasoning layer."""

    qualification_id: str
    qualification_name: str
    qp_code: str
    nsqf_level: int
    sector: str
    verification_status: VerificationStatus
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    relationship: str
    provenance: Provenance


class AIChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(min_length=1, max_length=4000)
    language: str = "hi"
    profile: Optional[LivelihoodProfile] = None


class AIChatResponse(BaseModel):
    session_id: str
    message: str
    language: str
    profile_updates: LivelihoodProfile
    candidate_pathways: list[CandidatePathway] = []
    evidence: list[EvidenceRecord] = []
    questions: list[str] = []
    next_step: str
    current_capabilities: list[str] = []
    transferable_skills: list[str] = []
    already_demonstrated: list[str] = []
    needs_verification: list[str] = []
    verified_gaps: list[str] = []
    provenance: list[Provenance] = []
    provider: str
    mode: str
    warnings: list[str] = []
