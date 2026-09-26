# PATHWAY ENGINE

## Purpose

Convert structured beneficiary evidence into a transparent set of 0–3 supported candidate pathways.

## Inputs

- normalized skills
- skill evidence
- interests
- education
- mobility/access constraints
- employment preference
- physical constraints where relevant
- canonical qualification data
- training capacity
- opportunity evidence.

## Output

Each candidate contains:

```text
pathway
qualification
supporting skills
missing skills
eligibility result
access result
capacity status
opportunity evidence status
exclusion risks
explanation
```

## Algorithm boundary

The engine must be deterministic.

LLM outputs are inputs, never final decisions.

## Candidate generation

1. Retrieve canonical pathways.
2. Filter invalid/unverified qualification records.
3. Evaluate explicit eligibility rules.
4. Normalize beneficiary skills.
5. Compare beneficiary skills with required competencies.
6. Identify skill gaps.
7. Apply access constraints.
8. inspect training-capacity evidence.
9. inspect opportunity-evidence status.
10. produce supported candidates.
11. sort using an approved deterministic rule.
12. return at most 3.

## Candidate count

```text
0 → no supported candidate
1 → return 1
2 → return 2
3+ → return max 3
```

## No fake score

Do not return a percentage match unless a real scoring model is designed, tested, and approved.

Prefer transparent evidence factors.

## Example explanation

```text
Supported because:
- beneficiary reported tractor repair experience
- mapped skill evidence overlaps with required competency X
- qualification is verified in canonical catalogue

Remaining gap:
- competency Y has no supporting evidence

Constraint:
- training capacity is currently insufficient in the selected district

Opportunity evidence:
- insufficient
```

## Exclusion reasons

Examples:
- qualification status unresolved
- eligibility not met
- required competency gap too large under approved rule
- mobility constraint
- missing critical evidence.

Do not hide exclusions.

## Stress test

Re-evaluate the candidate under:
- capacity reduced
- distance increased
- opportunity evidence removed
- one or more skills removed
- evidence marked missing.

This is deterministic scenario analysis, not employment prediction.
