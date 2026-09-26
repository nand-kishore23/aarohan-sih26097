import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import (
    Beneficiary, Qualification, CandidatePathway, 
    Provenance, ProvenanceOrigin, VerificationStatus
)
from app.skill_engine import extract_skills
from app.pathway_engine import evaluate_candidate, recommend_pathways

client = TestClient(app)

def test_extract_skills():
    text = "Main tractor aur pump repair karta hoon, papa ke saath kaam karta hoon."
    skills = extract_skills(text)
    
    assert len(skills) >= 2
    skill_names = [s.normalized_skill for s in skills]
    assert "tractor_repair" in skill_names
    assert "pump_repair" in skill_names
    
    # Check provenance
    for skill in skills:
        assert skill.source_type == ProvenanceOrigin.SELF_REPORTED

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_interview_flow():
    req = {
        "text": "Tractor aur machine repair karta hoon",
        "demo_mode": True
    }
    resp = client.post("/api/demo/interview", json=req)
    assert resp.status_code == 200
    data = resp.json()
    assert data["beneficiary"]["raw_statement"] == req["text"]
    assert len(data["skills"]) > 0

def test_pathway_evaluation():
    # Setup mock qual
    qual = Qualification(
        id="test-1", qp_code="TEST/001", name="Test Qual",
        required_skills=["skill1", "skill2", "skill3"]
    )
    
    # Setup mock ben
    ben = Beneficiary(id="ben-1", skills=[])
    from app.models import SkillObservation
    ben.skills.append(SkillObservation(
        raw_skill="skill1", normalized_skill="skill1", evidence_text="",
        source_type=ProvenanceOrigin.SELF_REPORTED,
        provenance=Provenance(origin=ProvenanceOrigin.SELF_REPORTED)
    ))
    
    candidate = evaluate_candidate(ben, qual)
    assert candidate is not None
    assert len(candidate.supporting_skills) == 1
    assert "skill1" in candidate.supporting_skills
    assert len(candidate.skill_gaps) == 2
