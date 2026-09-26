import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.api import router as api_router

app = FastAPI(title="AAROHAN Prototype API", version="0.1.0")

local_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
configured_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
allowed_origins = list(dict.fromkeys([*local_origins, *configured_origins]))

# Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
