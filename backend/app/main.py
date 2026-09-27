import os
import time
from threading import Lock

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes.api import router as api_router
from .services.latency import elapsed_ms, log_latency

app = FastAPI(title="AAROHAN Prototype API", version="0.1.0")
_ai_chat_request_lock = Lock()
_last_ai_chat_started_at: float | None = None


@app.middleware("http")
async def log_ai_chat_request_latency(request: Request, call_next):
    """Log end-to-end chat timing and a process-local idle/warm indicator."""

    global _last_ai_chat_started_at
    if request.url.path != "/api/ai/chat":
        return await call_next(request)

    started_at = time.perf_counter()
    with _ai_chat_request_lock:
        previous_started_at = _last_ai_chat_started_at
        _last_ai_chat_started_at = started_at
    lifecycle = "first_in_process" if previous_started_at is None else "warm"
    idle_ms = None if previous_started_at is None else round((started_at - previous_started_at) * 1000)
    request.state.ai_chat_started_at = started_at
    request.state.ai_chat_lifecycle = lifecycle

    try:
        response = await call_next(request)
    finally:
        total_ms = elapsed_ms(started_at)
        log_latency("ai_chat", "total", total_ms, lifecycle=lifecycle, idle_ms=idle_ms)
        endpoint_finished_at = getattr(request.state, "ai_chat_endpoint_finished_at", None)
        if endpoint_finished_at is not None:
            log_latency(
                "ai_chat",
                "response_serialization",
                elapsed_ms(endpoint_finished_at),
            )
    return response

local_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
configured_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
allowed_origins = list(dict.fromkeys([*local_origins, *configured_origins]))
vercel_aarohan_origin_regex = r"^https://aarohan-sih26097(?:-[a-z0-9-]+)?\.vercel\.app$"

# Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=vercel_aarohan_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Aarohan backend is healthy"}

@app.get("/api/v1/health")
def api_health_check():
    return {"status": "ok", "message": "Aarohan backend is healthy"}

app.include_router(api_router)
