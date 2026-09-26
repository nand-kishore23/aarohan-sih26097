# FIRST CODEX / ANTIGRAVITY IMPLEMENTATION PROMPT

You are the implementation engineer for AAROHAN.

Before doing anything:

1. Read `AGENTS.md`.
2. Read `docs/00_MASTER_SPEC.md`.
3. Read `docs/12_DECISIONS.md`.
4. Read `docs/13_BUILD_RULES.md`.
5. Inspect the repository.

## TASK

Implement ONLY the repository foundation.

Create a clean development foundation for:

- Next.js frontend
- FastAPI backend
- PostgreSQL configuration
- Docker development environment
- environment-variable templates
- basic health-check endpoints
- basic frontend/backend connectivity.

## DO NOT IMPLEMENT YET

Do not implement:
- pathway matching
- qualification matching
- voice AI
- LLM integration
- synthetic beneficiary generation
- dashboards
- evidence brief
- government integrations
- WhatsApp
- IVR
- authentication beyond the minimum development shell
- production deployment complexity.

## REQUIRED STRUCTURE

Preserve:

```text
AAROHAN/
├── AGENTS.md
├── README.md
├── CHANGELOG.md
├── DO_NOT_INVENT.md
├── docs/
├── data/
├── frontend/
├── backend/
└── scripts/
```

Do not delete existing specification files.

## BACKEND

Create:
- FastAPI application
- `/health`
- `/api/v1/health`
- environment configuration
- structured error handling foundation
- test setup.

Do not create domain logic yet.

## FRONTEND

Create:
- Next.js application shell
- a minimal home page identifying Aarohan
- backend health status display through a safe API call or configured proxy
- no product dashboard yet.

## DATABASE

Create:
- PostgreSQL development configuration
- connection configuration
- migration framework foundation.

Do NOT finalize the Aarohan domain schema yet. The qualification catalogue validation gate is still open.

## DOCKER

Provide a local development environment that can run:
- frontend
- backend
- PostgreSQL.

Do not add unnecessary services.

## CONFIGURATION

Create `.env.example` files.

Never commit secrets.

## TESTS

Add minimal tests proving:
- backend health endpoint works
- frontend build/lint/type checks can run
- database configuration is syntactically valid.

## ACCEPTANCE CRITERIA

1. `docker compose up` can start the development stack, subject to local Docker availability.
2. Backend health endpoint returns a successful structured response.
3. Frontend starts successfully.
4. Frontend can report backend health.
5. PostgreSQL is available as a development dependency.
6. No fake external integrations exist.
7. No qualification data is invented.
8. Existing documentation remains unchanged.
9. Tests pass.
10. CHANGELOG.md records the implementation.

## OUTPUT

After implementation report:

```text
FILES CHANGED:
...

COMMANDS RUN:
...

TESTS:
...

KNOWN LIMITATIONS:
...

NEXT RECOMMENDED TASK:
...
```

Do not continue into the next subsystem automatically.
