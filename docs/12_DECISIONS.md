# ARCHITECTURAL DECISION LOG

## ADR-001 — Product concept frozen

Status: FINAL

The Aarohan product concept is frozen. Engineering work must implement it rather than redesign it.

## ADR-002 — Decision-support, not autonomous government decision-maker

Status: FINAL

Aarohan provides evidence and candidate pathways. Human review remains required.

## ADR-003 — LLM cannot make deterministic pathway decisions

Status: FINAL

LLM handles language and explanation. Deterministic backend owns rules and calculations.

## ADR-004 — Candidate pathways are 0–3

Status: FINAL

Never force exactly three.

## ADR-005 — No fabricated opportunity scores

Status: FINAL

Opportunity evidence is evidence-backed or explicitly insufficient/synthetic.

## ADR-006 — Unknown is unknown

Status: FINAL

Unknown is neither low nor high and must not become an estimate.

## ADR-007 — Synthetic data is always labelled

Status: FINAL

Synthetic beneficiary and opportunity data must be visibly labelled.

## ADR-008 — NCS is not an MVP API dependency

Status: FINAL

No live NCS dependency unless a real authorized interface is implemented.

## ADR-009 — Digital Services is not an MVP umbrella pathway

Status: FINAL

Generic digital-services recommendation is too broad.

## ADR-010 — Formal pathways require source validation

Status: FINAL

A pathway is eligible for canonical use only after source/status/NOS/competency validation.

## ADR-011 — 500 synthetic beneficiaries for MVP

Status: FINAL

Use approximately 500 synthetic profiles for district intelligence demonstration.

## ADR-012 — Evidence Brief is a primary government-facing output

Status: FINAL

It is an AI-assisted analytical brief, not an official PM-AJAY plan.

## ADR-013 — Aarohan does not replace PM-AJAY MIS

Status: FINAL

Aarohan is an intelligence layer supporting planning and review.

## ADR-014 — No live government integration claim without implementation/authorization

Status: FINAL

Do not imply integration merely because an architecture has an adapter.

## ADR-015 — Raw-to-canonical ingestion

Status: FINAL

External records follow:

```text
SOURCE → RAW RECORD → NORMALIZATION → VALIDATION → CANONICAL RECORD
```

## ADR-016 — Qualification identity includes record variant/version

Status: FINAL

QP code alone is insufficient where public source systems expose multiple records under the same code.

## ADR-017 — Canonical catalogue is an explicit artifact

Status: FINAL

`data/normalized/qualification_catalogue.json` is the deterministic engine's qualification source of truth.

## ADR-018 — Schema waits for qualification lock

Status: FINAL

Do not prematurely lock the production database schema around guessed competency structures.

## ADR-019 — No fake confidence percentage

Status: FINAL

Use evidence/provenance dimensions instead of unsupported AI confidence numbers.

## ADR-020 — Stress test is a view, not a separate AI subsystem

Status: FINAL

It re-evaluates existing deterministic data under controlled scenarios.

## ADR-021 — Product scope exclusions

Status: FINAL

No production WhatsApp, production IVR, giant GIS, business-plan generator, provider ranking, blockchain, employment prediction, budget generation, or fake API integrations in MVP.

## ADR-022 — Current pathway set is three candidates, not three forced outputs

Status: FINAL

Current candidates:
- AGR/Q1108 Tractor Mechanic
- ELE/Q3115 Multi Skill Technician (Electrical)
- QG-04-FI-02933-2024-V2-FICSI Dairy Product Processor

This is a data-validation state, not permission to invent alternatives to reach a count.

## ADR-023 — Conversation is not the source of truth

Status: FINAL

The repository specification and decision log are the engineering source of truth.

## ADR-024 — Significant coding changes require review

Status: FINAL

A coding-agent proposal that changes architecture, data assumptions, external integrations, or product scope must be reviewed against this decision log before acceptance.
