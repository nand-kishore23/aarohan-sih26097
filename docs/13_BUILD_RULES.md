# BUILD RULES

## Rule 1 — One subsystem at a time

Never ask a coding agent to build the entire platform in one uncontrolled pass.

## Rule 2 — Read before code

Always read:
- AGENTS.md
- MASTER SPEC
- DECISIONS
- relevant subsystem specification.

## Rule 3 — Inspect before modify

The coding agent must inspect existing code before editing.

## Rule 4 — Smallest implementation

Implement only the requested task.

## Rule 5 — No speculative infrastructure

Do not add:
- unused microservices
- unused APIs
- unused providers
- unused databases
- unused authentication systems.

## Rule 6 — Data before matching

Do not implement the final matching engine before the canonical qualification catalogue is locked.

## Rule 7 — Catalogue before schema

Do not freeze competency tables before actual source structure is known.

## Rule 8 — Test every deterministic rule

Any rule affecting a candidate pathway must have unit tests.

## Rule 9 — Provenance is part of the data model

Do not add provenance later as a cosmetic UI feature.

## Rule 10 — Synthetic data must be traceable

Seed data must have a generation version and explicit synthetic origin.

## Rule 11 — UI follows data

Do not build UI cards for fields that do not exist in the canonical data model.

## Rule 12 — No fake integrations

Adapters can exist, but the UI must not imply a live integration unless it works.

## Rule 13 — No silent product changes

If implementation pressure suggests a product change, stop and add a decision proposal instead.

## Rule 14 — Every task ends with evidence

Report:
- changed files
- commands run
- test results
- known limitations
- next task.

## Rule 15 — Change log

Update CHANGELOG.md after meaningful implementation changes.

## Recommended build order

```text
0. Master repository package
1. Qualification data extraction/audit
2. qualification_catalogue.json
3. Data model/schema
4. Repository foundation
5. Backend contracts
6. Beneficiary voice flow
7. Profile/extraction
8. Deterministic pathway engine
9. Evidence/explainability
10. District aggregation
11. Evidence Brief
12. Testing/hardening
13. Demo polish
```
