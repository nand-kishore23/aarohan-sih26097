# AAROHAN Backend AI Intelligence

The FastAPI backend keeps AAROHAN's deterministic catalogue, pathway engine, community engine, and Evidence Brief as the source of truth. The conversational layer understands beneficiary language, keeps a short session profile, calls deterministic evidence tools, and optionally asks Gemini to explain that grounded result in the beneficiary's language.

## Architecture

```text
voice/text -> capability extraction -> session profile -> deterministic evidence retrieval
           -> Gemini explanation (optional) -> conversational response
```

Gemini never owns pathway IDs, QP codes, NSQF levels, NOS, eligibility, capacity, opportunity signals, or skill-gap calculations. Those remain deterministic and carry provenance. Derived capabilities such as `mobile_phone_repair` are not qualification evidence.

## Configuration

Copy the root `.env.example` into the deployment environment. Do not commit a `.env` file.

```text
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash-lite
AI_PROVIDER=gemini
ASR_PROVIDER=browser_fallback
AI4BHARAT_MODEL=
AI4BHARAT_ENDPOINT=
```

`google-genai` is the official Google GenAI Python SDK. `GEMINI_MODEL` stays configurable because Gemini model availability and free-tier limits vary by model and can change. The default was selected because Google documented a free tier for Gemini 2.5 Flash-Lite at implementation time; it is not an unlimited or permanent free-use promise. If the key, SDK, or configured model is unavailable, chat returns the deterministic grounded fallback with a warning instead of inventing a result.

## API

- `GET /health` and existing `/api/v1/health`: backend health.
- `GET /api/ai/status`: safe provider, ASR, model, and evidence-engine status.
- `POST /api/ai/chat`: session-aware grounded conversation.
- `POST /api/ai/analyze`: same structured response for analysis-oriented clients.
- `POST /api/voice/transcribe`: optional server-side ASR or browser transcript relay.

`POST /api/ai/chat` accepts `session_id`, `message`, `language`, and an optional structured `profile`. It returns the session ID, language-aware answer, profile updates with provenance, candidate pathways, evidence, short clarification questions, next step, provider, and mode. It also separates `already_demonstrated` capabilities, derived `transferable_skills`, `needs_verification`, and `verified_gaps`; the latter remains empty while the prototype catalogue is only partially verified.

## ASR

The lightweight default is `ASR_PROVIDER=browser_fallback`, preserving the existing browser SpeechRecognition flow. Send its real transcript as multipart `fallback_text`; the backend never pretends to transcribe uploaded audio.

For AI4Bharat IndicConformer, set `ASR_PROVIDER=ai4bharat`, `AI4BHARAT_MODEL`, and `AI4BHARAT_ENDPOINT`. The endpoint must accept multipart field `audio` plus `model` and `language`, and return JSON with a non-empty `text` string. The model is not bundled or eager-loaded in Render: host it locally or behind a separately managed service sized for the selected model. This avoids making the Render Free web service unavailable because of a large ASR model.

## Render

Install `backend/requirements.txt` during the normal build. Secrets belong in Render environment variables only. Startup remains lightweight because Gemini and the optional ASR provider are created on request. Keep existing `CORS_ALLOWED_ORIGINS` for the Vercel frontend; no frontend architecture or voice UI change is required by these backend endpoints.

## Testing

From `backend`:

```powershell
python -m pytest
```

The suite covers the Gemini-disabled deterministic fallback, session-memory phone-repair conversation, Hindi/Hinglish/English capability extraction, voice fallback behavior, existing routes, community aggregation, and Evidence Brief. A Gemini-enabled request is only exercised when a deployment supplies a real key; never print that key in logs or tests.

## Prototype limits

The catalogue contains only the existing three partially verified prototype pathways. A phone-repair statement can be understood as a derived capability, but the backend will not manufacture a phone repair QP or NSQF level. It either asks a useful clarification question, identifies a demonstrably related verified prototype pathway, or states that evidence is insufficient. Human field and training centre validation remain required.
