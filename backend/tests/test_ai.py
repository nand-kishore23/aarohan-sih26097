import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import AIChatRequest
from app.services.ai.base import AIProvider
from app.services.ai.service import AIService, SessionStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def disabled_gemini(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("ASR_PROVIDER", "browser_fallback")


def test_ai_status_is_safe_and_reports_deterministic_fallback():
    response = client.get("/api/ai/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["ai_provider"] == "gemini"
    assert payload["ai_configured"] is False
    assert payload["mode"] == "deterministic_fallback"
    assert "GEMINI_API_KEY" not in str(payload)


def test_provider_abstraction_can_return_a_grounded_response():
    class StubProvider(AIProvider):
        name = "stub"

        @property
        def configured(self):
            return True

        def generate_response(self, request):
            assert request.questions
            assert request.profile.capabilities[0].capability == "mobile_phone_repair"
            return "Grounded provider response"

    response = AIService(provider=StubProvider(), sessions=SessionStore()).chat(
        AIChatRequest(message="Mujhe phone repair aata hai", language="hi")
    )

    assert response.provider == "stub"
    assert response.mode == "ai_grounded"
    assert response.message == "Grounded provider response"


def test_phone_repair_conversation_updates_profile_and_never_invents_pathway():
    service = AIService(sessions=SessionStore())

    first = service.chat(AIChatRequest(message="Mujhe phone repair aata hai", language="hi"))
    assert first.questions
    assert "mobile_phone_repair" in {item.capability for item in first.profile_updates.capabilities}
    assert not first.candidate_pathways
    assert first.provider == "deterministic_fallback"

    second = service.chat(
        AIChatRequest(
            session_id=first.session_id,
            message="Display aur charging ka repair karta hoon.",
            language="hi",
        )
    )
    capabilities = {item.capability for item in second.profile_updates.capabilities}
    assert {"display_replacement", "charging_fault_repair"}.issubset(capabilities)
    assert second.questions == ["Kya aap soldering bhi karte hain?"]

    third = service.chat(
        AIChatRequest(
            session_id=first.session_id,
            message="Soldering bhi kar leta hoon.",
            language="hi",
        )
    )
    capabilities = {item.capability for item in third.profile_updates.capabilities}
    assert "soldering" in capabilities
    assert third.questions == []
    assert all(path.qp_code == "ELE/Q3115" for path in third.candidate_pathways)
    assert all(evidence.qp_code == "ELE/Q3115" for evidence in third.evidence)
    assert third.verified_gaps == []
    assert "soldering" in third.already_demonstrated
    assert "formal phone-repair qualification" in third.message


@pytest.mark.parametrize(
    ("statement", "capability"),
    [
        ("Mujhe phone repair aata hai", "mobile_phone_repair"),
        ("Main mobile theek kar leta hoon", "mobile_phone_repair"),
        ("Display change kar deta hoon", "display_replacement"),
        ("Charging ka fault dekh leta hoon", "charging_fault_repair"),
        ("Papa ke saath tractor repair karta hoon", "tractor_repair"),
        ("Machine khol leta hoon aur problem samajh leta hoon", "machine_diagnostics"),
        ("I repair mobile phones", "mobile_phone_repair"),
        ("I replace phone displays", "display_replacement"),
    ],
)
def test_hindi_hinglish_and_english_capability_extraction(statement, capability):
    response = client.post("/api/ai/chat", json={"message": statement, "language": "hi"})

    assert response.status_code == 200
    capabilities = {item["capability"] for item in response.json()["profile_updates"]["capabilities"]}
    assert capability in capabilities


def test_voice_endpoint_relays_browser_transcript_without_fake_asr():
    response = client.post(
        "/api/voice/transcribe",
        data={"language": "hi", "fallback_text": "Mujhe phone repair aata hai"},
        files={"audio": ("sample.webm", b"placeholder", "audio/webm")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "text": "Mujhe phone repair aata hai",
        "language": "hi",
        "provider": "browser_fallback",
        "status": "fallback",
    }


def test_voice_endpoint_fails_clearly_without_a_real_transcript():
    response = client.post(
        "/api/voice/transcribe",
        data={"language": "hi"},
        files={"audio": ("sample.webm", b"placeholder", "audio/webm")},
    )

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "ASR_PROVIDER_UNAVAILABLE"


def test_existing_interview_pathway_and_community_routes_still_smoke():
    health = client.get("/health")
    interview = client.post(
        "/api/demo/interview",
        json={"text": "Main tractor aur pump repair karta hoon", "language": "hi"},
    )

    assert health.status_code == 200
    assert interview.status_code == 200
    beneficiary_id = interview.json()["beneficiary"]["id"]

    recommendations = client.post("/api/pathways/recommend", json={"beneficiary_id": beneficiary_id})
    assert recommendations.status_code == 200
    assert recommendations.json()["count"] >= 1

    pathway_id = recommendations.json()["pathways"][0]["id"]
    assert client.get(f"/api/pathways/{pathway_id}").status_code == 200
    assert client.get("/api/community/summary").status_code == 200
    assert client.get("/api/community/evidence-brief").status_code == 200
