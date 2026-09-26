# AAROHAN

**From Voice to Livelihood Intelligence**

Aarohan is a voice-first livelihood intelligence platform for SIH 2026 problem statement **SIH26097**. It converts beneficiary conversations into structured skills, evidence-informed candidate livelihood pathways, and aggregated district-level planning intelligence that can support PM-AJAY livelihood planning.

## Current status

- Product concept and pathway strategy: **FINAL**
- Application implementation: **SIH prototype complete**
- Qualification catalogue: **AUDIT / VALIDATION**; the prototype uses a preserved deterministic demonstration catalogue
- Persistence, live integrations, and production services: **OUT OF SCOPE FOR THIS PROTOTYPE**

## Source of truth

Coding agents must read:

1. `AGENTS.md`
2. `docs/00_MASTER_SPEC.md`
3. `docs/12_DECISIONS.md`
4. `docs/13_BUILD_RULES.md`
5. the relevant subsystem document before changing code.

The conversation is historical context. **The repository is the engineering source of truth.**

## Product flow

```text
VOICE
  ↓
SKILL
  ↓
PATHWAY
  ↓
EVIDENCE
  ↓
HUMAN DECISION
  ↓
PLANNING
```

## Engineering boundary

```text
LLM
= conversation, extraction, clarification, normalization assistance, explanation

DETERMINISTIC BACKEND
= qualification retrieval, matching, eligibility/rules, skill gaps,
  constraints, evidence status, aggregation, mismatch calculations

DATABASE
= structured source of truth

PROVENANCE
= trust layer
```

## Never invent

See `DO_NOT_INVENT.md`.

If data is unavailable, use **UNKNOWN / MISSING**. Never fill a gap with plausible-looking government data.

## First build task

Use the prompt in `docs/14_FIRST_CODEX_PROMPT.md`.
