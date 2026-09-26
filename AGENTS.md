# AAROHAN ENGINEERING RULES

You are implementing AAROHAN, an already-approved SIH 2026 solution.

## REQUIRED READING

Before modifying code, read:

1. `AGENTS.md`
2. `docs/00_MASTER_SPEC.md`
3. `docs/12_DECISIONS.md`
4. `docs/13_BUILD_RULES.md`
5. the subsystem specification relevant to the task.

Do not rely on the chat history when the repository contains the relevant decision.

## PRODUCT IS FROZEN

Do not redesign, rename, broaden, simplify, or reinterpret the product without an explicit decision recorded in `docs/12_DECISIONS.md`.

Do not turn Aarohan into:
- a generic chatbot,
- a course marketplace,
- a PM-AJAY MIS replacement,
- an autonomous government decision-maker,
- an employment prediction engine.

## DATA INTEGRITY

Never invent:
- QP codes
- NOS codes
- NSQF levels
- qualification status
- qualification competencies
- eligibility requirements
- assessment rules
- government statistics
- training-provider capacity
- vacancies
- employer demand
- government APIs
- official partnerships
- PM-AJAY integrations
- Skill India integrations
- NCS integrations.

If a value is unavailable, represent it as missing/unknown.

## AI BOUNDARIES

LLM may perform:
- speech/transcript interpretation
- conversation
- clarification
- extraction from beneficiary language
- skill-normalization assistance
- explanation of deterministic results.

LLM must NOT perform:
- eligibility decisions
- qualification creation
- QP/NOS invention
- NSQF assignment
- pathway invention
- opportunity calculation
- training-capacity calculation
- district aggregation
- final government decisions.

Those belong to deterministic backend logic backed by canonical data.

## PROVENANCE

Every important fact must have provenance.

Allowed origins:

- `SOURCE_BACKED`
- `SELF_REPORTED`
- `DERIVED`
- `SYNTHETIC`
- `MISSING`

Synthetic data must be visibly labelled in the UI.

## UNKNOWN RULE

Unknown is not low.
Unknown is not high.
Unknown is not an estimate.

```text
UNKNOWN = UNKNOWN
```

Do not convert missing evidence into a score.

## EXTERNAL SOURCES

Never create a fake API integration.

If an external integration is not actually implemented and authorized:
- do not claim it is live,
- do not create fake API responses,
- use an adapter boundary or clearly labelled synthetic fixture.

## IMPLEMENTATION DISCIPLINE

For every task:

1. Read the relevant specification.
2. Inspect the existing repository.
3. Make the smallest change satisfying the specification.
4. Do not add unrelated features.
5. Run tests/lint/type checks.
6. Report files changed.
7. Report tests run and results.
8. Report limitations.
9. Update `CHANGELOG.md`.

If the specification conflicts with the code, stop and report the conflict instead of silently changing the product.

## DATABASE RULE

Do not lock the production schema around guessed qualification fields before `qualification_catalogue.json` is validated.

## UI RULE

Never render a field merely because a UI card looks better with it.

No data -> no fabricated card.

Use:
- `MISSING`
- `UNKNOWN`
- `SOURCE-BACKED`
- `SELF-REPORTED`
- `DERIVED`
- `SYNTHETIC`

## SECURITY / PRIVACY

Do not expose beneficiary personal data in district aggregation.
Use aggregation and anonymization boundaries.
Do not log raw voice recordings or sensitive profile fields unnecessarily.
Do not place secrets in source code.

## STOP CONDITIONS

Stop and ask for review if:
- a requested feature is not in the approved specification,
- an external API is unavailable,
- source data is ambiguous,
- a qualification has conflicting versions/statuses,
- an implementation would require fabricated data,
- a proposed change alters the frozen product concept.
