# ARCHITECTURE

## Logical architecture

```text
                    AAROHAN
                       │
             ┌─────────┴─────────┐
             │                   │
       BENEFICIARY          GOVERNMENT
             │                   │
             ↓                   ↓
           VOICE          DISTRICT SIGNALS
             │                   │
             ↓                   ↓
       STRUCTURED DATA       AGGREGATION
             │                   │
             └─────────┬─────────┘
                       ↓
                PATHWAY ENGINE
                       ↓
                EVIDENCE ENGINE
                       ↓
                 HUMAN DECISION
                       ↓
                 EVIDENCE BRIEF
```

## Technical layers

```text
Frontend
  ↓
API
  ↓
Application services
  ├── Conversation service
  ├── Profile extraction service
  ├── Qualification catalogue service
  ├── Pathway engine
  ├── Evidence service
  ├── Aggregation service
  └── Evidence brief service
  ↓
PostgreSQL
  ├── raw/source records
  ├── canonical qualification catalogue
  ├── beneficiary profiles
  ├── skill observations
  ├── training capacity
  ├── opportunity signals
  └── derived district signals
```

## Raw-to-canonical data pipeline

```text
SOURCE
 ↓
RAW RECORD
 ↓
NORMALIZATION
 ↓
VALIDATION
 ↓
CANONICAL RECORD
```

Never directly write scraped/source text into production canonical tables.

## LLM boundary

```text
VOICE
 ↓
ASR
 ↓
LLM conversation/extraction
 ↓
structured candidate facts
 ↓
deterministic validation
 ↓
canonical data
 ↓
pathway engine
 ↓
explanation
```

## Community branch

```text
profiles
 ↓
anonymized aggregation
 ↓
observed interest
 ↓
capacity
 ↓
opportunity evidence
 ↓
potential mismatch
```

Community intelligence must never directly decide an individual pathway.

## Deployment target

MVP should be deployable locally and in a standard web environment using:
- frontend container/runtime
- FastAPI backend
- PostgreSQL
- environment-based configuration.

Docker development environment is preferred.
