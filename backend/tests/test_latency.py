import logging

from app.services.latency import timed


def test_timed_logs_a_named_stage_without_payload_content(caplog):
    caplog.set_level(logging.INFO, logger="aarohan.latency")

    with timed("ai_chat", "profile_prepare", lifecycle="warm"):
        pass

    assert "[LATENCY] ai_chat profile_prepare_ms=" in caplog.text
    assert "lifecycle=warm" in caplog.text
