import uuid
from datetime import datetime
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..models import (
    InterviewRequest, InterviewResponse, Beneficiary,
    PathwayRecommendRequest, PathwayRecommendResponse,
    PathwayDecisionRequest, PathwayDecisionResponse, AIChatRequest, AIChatResponse
)
from ..skill_engine import extract_skills
from ..pathway_engine import recommend_pathways
from ..services.ai.service import ai_service
from ..services.asr.base import ASRProviderUnavailableError
from ..services.asr.service import asr_service
from ..seed_data import (
    beneficiaries, QUALIFICATION_CATALOGUE, DEMO_BENEFICIARY,
    pathway_results, decisions
)

router = APIRouter()

@router.post("/api/demo/interview", response_model=InterviewResponse)
def run_interview(req: InterviewRequest):
    """
    Simulates a voice interview processing step.
    For the prototype, if demo_mode is True, it processes the text,
    builds the demo beneficiary, extracts skills, and saves it.
    """
    # 1. Start with the template demo beneficiary (provides structural defaults)
    ben = DEMO_BENEFICIARY.model_copy(deep=True)
    
    # 2. Update with the actual text submitted
    ben.raw_statement = req.text
    ben.id = f"ben-{uuid.uuid4().hex[:8]}"
    
    # 3. Extract skills deterministically
    skills = extract_skills(req.text)
    ben.skills = skills
    
    # 4. Derive livelihood and interests from extracted skills so the
    #    profile reflects what the user actually reported rather than
    #    inheriting stale demo seed data.
    from ..models import ProvenanceOrigin
    if skills:
        readable = [s.normalized_skill.replace("_", " ") for s in skills]
        ben.current_livelihood = ", ".join(dict.fromkeys(readable))
        ben.interests = list(dict.fromkeys(readable))
        ben.work_experience = ""  # clear demo boilerplate
        ben.data_origin = ProvenanceOrigin.SELF_REPORTED
    
    # 5. Save to in-memory store
    beneficiaries[ben.id] = ben
    
    return InterviewResponse(
        interview_id=f"int-{uuid.uuid4().hex[:8]}",
        beneficiary=ben,
        skills=skills
    )

@router.get("/api/beneficiaries/{ben_id}", response_model=Beneficiary)
def get_beneficiary(ben_id: str):
    ben = beneficiaries.get(ben_id)
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return ben

@router.post("/api/pathways/recommend", response_model=PathwayRecommendResponse)
def recommend(req: PathwayRecommendRequest):
    ben = beneficiaries.get(req.beneficiary_id)
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
        
    candidates = recommend_pathways(ben, QUALIFICATION_CATALOGUE)
    
    # Store for later retrieval by ID
    for c in candidates:
        pathway_results[c.id] = c
        
    return PathwayRecommendResponse(
        beneficiary_id=ben.id,
        pathways=candidates,
        count=len(candidates)
    )

@router.get("/api/pathways/{pathway_id}")
def get_pathway(pathway_id: str):
    candidate = pathway_results.get(pathway_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Pathway not found")
        
    # Also fetch the full qualification details to enrich the response
    qual = QUALIFICATION_CATALOGUE.get(candidate.qualification_id)
    
    return {
        "candidate": candidate,
        "qualification": qual
    }

@router.post("/api/pathways/{pathway_id}/decision", response_model=PathwayDecisionResponse)
def record_decision(pathway_id: str, req: PathwayDecisionRequest):
    if pathway_id not in pathway_results:
        raise HTTPException(status_code=404, detail="Pathway not found")
        
    decision_record = {
        "pathway_id": pathway_id,
        "decision": req.decision.value,
        "notes": req.notes,
        "recorded_at": datetime.now().isoformat()
    }
    
    decisions[pathway_id] = decision_record
    
    return PathwayDecisionResponse(
        pathway_id=pathway_id,
        decision=req.decision,
        recorded_at=decision_record["recorded_at"]
    )

@router.get("/api/qualifications")
def list_qualifications():
    return list(QUALIFICATION_CATALOGUE.values())

@router.get("/api/qualifications/{qual_id}")
def get_qualification(qual_id: str):
    qual = QUALIFICATION_CATALOGUE.get(qual_id)
    if not qual:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return qual

@router.get("/api/community/summary")
def get_community_summary():
    from ..community_engine import aggregate_community_intelligence
    return aggregate_community_intelligence()

@router.get("/api/community/evidence-brief")
def get_evidence_brief():
    from ..community_engine import generate_evidence_brief
    return generate_evidence_brief()


@router.get("/api/ai/status")
def get_ai_status():
    """Expose deployment-safe configuration state without revealing credentials."""
    return ai_service.status()


@router.post("/api/ai/chat", response_model=AIChatResponse)
def chat_with_ai(req: AIChatRequest):
    """Run grounded conversational reasoning with session-level profile memory."""
    return ai_service.chat(req)


@router.post("/api/ai/analyze", response_model=AIChatResponse)
def analyze_with_ai(req: AIChatRequest):
    """Compatibility endpoint for clients that request a structured AI analysis."""
    return ai_service.chat(req)


@router.post("/api/voice/transcribe")
async def transcribe_voice(
    audio: UploadFile = File(...),
    language: str = Form("hi"),
    fallback_text: str | None = Form(None),
):
    """Transcribe through configured ASR, or relay an existing browser transcript."""
    try:
        audio_bytes = await audio.read()
        return asr_service.transcribe(
            audio=audio_bytes,
            filename=audio.filename or "audio",
            content_type=audio.content_type or "application/octet-stream",
            language=language,
            fallback_text=fallback_text,
        )
    except ASRProviderUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail={"code": "ASR_PROVIDER_UNAVAILABLE", "message": str(exc)},
        ) from exc
