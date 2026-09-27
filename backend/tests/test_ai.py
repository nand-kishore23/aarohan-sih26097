import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import AIChatRequest
from app.services.ai.base import AIProvider, AIProviderUnavailableError
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


class StructuredUnderstandingProvider(AIProvider):
    name = "gemini"

    def __init__(self, understandings):
        self.understandings = understandings
        self.explanation_requests = []

    @property
    def configured(self):
        return True

    def understand(self, request):
        return self.understandings[request.message]

    def generate_response(self, request):
        self.explanation_requests.append(request)
        return "Grounded explanation from deterministic AAROHAN evidence."


def test_gemini_structured_understanding_is_primary_for_phone_repair_multi_turn():
    provider = StructuredUnderstandingProvider(
        {
            "Mujhe phone repair aata hai.": {
                "language": "hi",
                "reported_tasks": ["phone repair"],
                "capabilities": ["mobile_phone_repair"],
                "missing_information": ["repair scope"],
                "clarification_question": "Phone mein aap kis tarah ka repair karte hain - display, charging, software, ya soldering?",
            },
            "Display aur charging ka repair karta hoon.": {
                "language": "hi",
                "reported_tasks": ["display repair", "charging repair"],
                "capabilities": ["display_replacement", "charging_fault_repair"],
                "missing_information": ["soldering experience"],
                "clarification_question": "Kya aap soldering bhi karte hain?",
            },
            "Soldering bhi kar leta hoon.": {
                "language": "hi",
                "reported_tasks": ["soldering"],
                "capabilities": ["soldering"],
            },
        }
    )
    service = AIService(provider=provider, sessions=SessionStore())

    first = service.chat(AIChatRequest(message="Mujhe phone repair aata hai.", language="hi"))
    assert first.provider == "gemini"
    assert first.mode == "ai_grounded"
    assert first.questions
    assert first.candidate_pathways == []
    assert first.profile_updates.self_reported_statements[0].provenance.origin == "SELF_REPORTED"
    assert first.profile_updates.capabilities[0].provenance.origin == "DERIVED"

    second = service.chat(
        AIChatRequest(
            session_id=first.session_id,
            message="Display aur charging ka repair karta hoon.",
            language="hi",
        )
    )
    third = service.chat(
        AIChatRequest(
            session_id=first.session_id,
            message="Soldering bhi kar leta hoon.",
            language="hi",
        )
    )

    capability_names = {item.capability for item in third.profile_updates.capabilities}
    assert {"mobile_phone_repair", "display_replacement", "charging_fault_repair", "soldering"}.issubset(capability_names)
    assert len(third.profile_updates.raw_statements) == 3
    assert len(third.profile_updates.self_reported_statements) == 3
    assert all(item.provenance.origin == "SELF_REPORTED" for item in third.profile_updates.self_reported_statements)
    assert all(item.provenance.origin == "DERIVED" for item in third.profile_updates.capabilities)
    assert all(path.qp_code == "ELE/Q3115" for path in third.candidate_pathways)
    assert all(evidence.qp_code == "ELE/Q3115" for evidence in third.evidence)
    assert third.verified_gaps == []
    assert "phone-repair" not in third.message.lower()
    assert provider.explanation_requests[-1].accepted_capabilities == [
        "mobile_phone_repair",
        "display_replacement",
        "charging_fault_repair",
        "soldering",
    ]


@pytest.mark.parametrize(
    ("message", "understanding", "expected_capabilities", "expected_qp"),
    [
        (
            "Mujhe phone repair aata hai.",
            {"language": "hi", "capabilities": ["mobile_phone_repair"]},
            {"mobile_phone_repair"},
            None,
        ),
        (
            "Bijli ka kaam seekha hai, fan aur geyser banata hoon. LED bhi theek kar leta hoon.",
            {"language": "hi", "capabilities": ["electrical_repair", "appliance_repair"]},
            {"electrical_repair", "appliance_repair"},
            "ELE/Q3115",
        ),
        (
            "Dairy mein kaam kiya hai, doodh ka testing aur pasteurization aata hai.",
            {"language": "hi", "capabilities": ["dairy_processing", "milk_testing", "pasteurization"]},
            {"dairy_processing", "milk_testing", "pasteurization"},
            "QG-04-FI-02933-2024-V2-FICSI",
        ),
    ],
)
def test_mocked_gemini_understanding_handles_hindi_without_keyword_expansion(
    message,
    understanding,
    expected_capabilities,
    expected_qp,
):
    provider = StructuredUnderstandingProvider({message: understanding})
    response = AIService(provider=provider, sessions=SessionStore()).chat(
        AIChatRequest(message=message, language="hi")
    )

    observed = {item.capability for item in response.profile_updates.capabilities}
    assert expected_capabilities.issubset(observed)
    if expected_qp:
        assert any(path.qp_code == expected_qp for path in response.candidate_pathways)
    else:
        assert response.candidate_pathways == []


def test_unknown_gemini_capability_becomes_unresolved_skill_without_matching():
    message = "Main advanced phone diagnostics karta hoon."
    provider = StructuredUnderstandingProvider(
        {message: {"language": "hi", "capabilities": ["advanced_phone_diagnostics"]}}
    )
    response = AIService(provider=provider, sessions=SessionStore()).chat(
        AIChatRequest(message=message, language="hi")
    )

    unresolved = [item for item in response.profile_updates.capabilities if item.capability == "UNRESOLVED_SKILL"]
    assert len(unresolved) == 1
    assert unresolved[0].normalized_from == "advanced_phone_diagnostics"
    assert response.candidate_pathways == []
    assert response.profile_updates.skills == []


def test_malicious_structured_output_cannot_introduce_qualification_or_opportunity_facts():
    message = "Mujhe phone repair aata hai."
    provider = StructuredUnderstandingProvider(
        {
            message: {
                "language": "hi",
                "capabilities": ["mobile_phone_repair"],
                "qp_code": "XYZ123",
                "nsqf_level": 7,
                "nos_code": "FAKE/NOS",
                "qualification": "Certified Phone Repair Technician",
                "opportunity": "100 local employers are hiring",
            }
        }
    )
    response = AIService(provider=provider, sessions=SessionStore()).chat(
        AIChatRequest(message=message, language="hi")
    )
    rendered = json.dumps(response.model_dump(mode="json"))

    assert "XYZ123" not in rendered
    assert "FAKE/NOS" not in rendered
    assert "Certified Phone Repair Technician" not in rendered
    assert "100 local employers are hiring" not in rendered
    assert response.candidate_pathways == []
    assert "Gemini structured understanding failed validation" in " ".join(response.warnings)


def test_gemini_understanding_unavailable_uses_existing_keyword_fallback_without_crashing():
    class UnavailableProvider(AIProvider):
        name = "gemini"

        @property
        def configured(self):
            return True

        def understand(self, request):
            raise AIProviderUnavailableError("simulated Gemini outage")

        def generate_response(self, request):
            raise AIProviderUnavailableError("simulated Gemini outage")

    response = AIService(provider=UnavailableProvider(), sessions=SessionStore()).chat(
        AIChatRequest(message="Main tractor aur pump repair karta hoon.", language="hi")
    )

    assert response.provider == "deterministic_fallback"
    assert response.mode == "deterministic_fallback"
    assert {"tractor_repair", "pump_repair"}.issubset(
        {item.capability for item in response.profile_updates.capabilities}
    )
    assert response.candidate_pathways
    assert "Gemini structured understanding was unavailable" in " ".join(response.warnings)
