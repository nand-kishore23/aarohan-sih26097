"""Deterministic Pathway Matching Engine."""
import uuid

from .models import (
    Beneficiary, CandidatePathway, Qualification,
    Provenance, ProvenanceOrigin, VerificationStatus
)


def evaluate_candidate(
    beneficiary: Beneficiary, qual: Qualification
) -> CandidatePathway | None:
    """Evaluates a single qualification against a beneficiary."""
    
    # 1. Eligibility Check (Simplified for prototype)
    # If the user says 10th pass, and qual needs 12th, we might flag it.
    # We will pass everyone for now but add a constraint note if it's Dairy (12th pass).
    access_constraints = []
    if qual.qp_code == "QG-04-FI-02933-2024-V2-FICSI" and "10th" in beneficiary.education.lower():
        # Requires 12th OR 10th + 2 years exp
        access_constraints.append("Eligibility warning: Requires 2 years experience for 10th pass")

    # 2. Skill Matching
    ben_skills = {obs.normalized_skill for obs in beneficiary.skills}
    qual_skills = set(qual.required_skills)
    
    supporting_skills = list(ben_skills.intersection(qual_skills))
    skill_gaps = list(qual_skills.difference(ben_skills))
    
    # If they have 0 overlapping skills, they might not be a candidate
    # (But for demo, we might want to return it anyway to show gaps if it's the only one. 
    # Let's say minimum 1 matching skill to be considered a candidate)
    if not supporting_skills:
        return None

    # 3. Generate Why This / Why Not
    why_this = [f"Matches beneficiary skill: {s.replace('_', ' ')}" for s in supporting_skills]
    why_not = []
    
    if len(skill_gaps) > 3:
        why_not.append(f"Significant skill gaps: Missing {len(skill_gaps)} required competencies")
        
    if "certificate nahi hai" in beneficiary.raw_statement.lower():
         why_not.append("Missing formal certification")

    # 4. Construct Candidate Pathway
    candidate = CandidatePathway(
        id=str(uuid.uuid4()),
        pathway_name=qual.display_name or qual.name,
        qp_code=qual.qp_code,
        nsqf_level=qual.nsqf_level,
        sector=qual.sector_council,
        supporting_skills=supporting_skills,
        skill_gaps=skill_gaps,
        access_constraints=access_constraints,
        evidence_status="PARTIALLY_VERIFIED",
        why_this=why_this,
        why_not=why_not,
        qualification_id=qual.id,
        provenance=Provenance(
            origin=ProvenanceOrigin.DERIVED,
            verification_status=VerificationStatus.PARTIALLY_VERIFIED
        )
    )
    
    return candidate


def recommend_pathways(
    beneficiary: Beneficiary, catalogue: dict[str, Qualification]
) -> list[CandidatePathway]:
    """
    Evaluates all qualifications and returns top 0-3 candidates.
    """
    candidates = []
    
    for qual in catalogue.values():
        candidate = evaluate_candidate(beneficiary, qual)
        if candidate:
            candidates.append(candidate)
            
    # Sort by number of supporting skills descending
    candidates.sort(key=lambda c: len(c.supporting_skills), reverse=True)
    
    # Return at most 3
    return candidates[:3]
