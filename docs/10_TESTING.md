# TESTING

## Unit tests

### Qualification catalogue

- QP code uniqueness within canonical identity/version rules.
- status validation.
- NSQF level type/range.
- source URL/reference presence.
- missing-field behavior.

### Pathway engine

Test:
- 0 candidates.
- 1 candidate.
- 2 candidates.
- 3 candidates.
- more than 3 candidates.
- invalid qualification.
- missing competency evidence.
- access constraint.
- insufficient opportunity evidence.
- capacity change alters mismatch.

### Provenance

Test:
- source-backed record displays source-backed.
- self-reported stays self-reported.
- derived result is marked derived.
- synthetic stays synthetic.
- missing is never rendered as a numerical estimate.

### Aggregation

Given a fixed seed dataset:
- observed interest counts are reproducible.
- capacity is summed correctly.
- mismatch calculation is deterministic.

## Integration tests

- interview → structured profile.
- profile → deterministic pathway engine.
- pathway → evidence explanation.
- profile dataset → district aggregation.
- aggregation → evidence brief.

## Guardrail tests

Ensure LLM cannot:
- create a new QP code,
- change NSQF level,
- mark an unverified qualification as validated,
- invent opportunity evidence,
- invent training capacity.

## UI tests

- provenance badges visible.
- synthetic warning visible.
- 0–3 candidate rule.
- no fake confidence percentages.
- unknown values show as missing/unknown.
