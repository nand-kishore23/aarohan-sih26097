# API CONTRACTS

API implementation begins after the data model and qualification catalogue are locked.

## Beneficiary APIs

### POST /api/v1/interviews

Starts or records an interview session.

### POST /api/v1/interviews/{id}/turns

Accepts transcript/audio metadata and returns the next conversational action.

### GET /api/v1/beneficiaries/{id}/profile

Returns structured profile with provenance.

### GET /api/v1/beneficiaries/{id}/pathways

Returns 0–3 deterministic candidate pathways.

### GET /api/v1/beneficiaries/{id}/pathways/{pathway_id}/stress-test

Returns deterministic scenario analysis.

## Government APIs

### GET /api/v1/districts/{district_id}/signals

Returns aggregated observed-interest and capacity signals.

### GET /api/v1/districts/{district_id}/mismatches

Returns potential interest-capacity mismatches.

### GET /api/v1/districts/{district_id}/evidence-brief

Returns the analytical brief data.

## Catalogue APIs

### GET /api/v1/qualifications

Returns canonical validated qualifications only.

### GET /api/v1/qualifications/{id}

Returns qualification, NOS, competency, eligibility and provenance.

## API rules

- Return provenance.
- Never return fabricated data.
- Use explicit null/missing status.
- Do not expose raw beneficiary data through aggregation endpoints.
- Do not expose secrets.
- Validate all LLM-produced structured input before persistence.

## Error semantics

Use machine-readable errors such as:

- `QUALIFICATION_NOT_VALIDATED`
- `SOURCE_CONFLICT`
- `MISSING_REQUIRED_EVIDENCE`
- `NO_SUPPORTED_PATHWAY`
- `OPPORTUNITY_EVIDENCE_INSUFFICIENT`
- `SYNTHETIC_DATA_ONLY`
