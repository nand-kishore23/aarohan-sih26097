# DO NOT INVENT

Aarohan is a traceable decision-support system.

Never invent:

- QP codes
- NOS codes
- NSQF levels
- qualification names
- qualification status
- qualification version
- NOS competencies
- performance criteria
- knowledge requirements
- eligibility
- assessment rules
- training hours
- training-provider data
- available seats
- vacancies
- employer demand
- wage figures
- employment probabilities
- district labour-market statistics
- PM-AJAY rules
- PM-AJAY portal APIs
- Skill India APIs
- NCS APIs
- government partnerships
- official integrations.

## Required behavior

If unavailable:

```json
{
  "value": null,
  "provenance": {
    "origin": "MISSING",
    "verification_status": "UNVERIFIED"
  }
}
```

If derived:

```text
origin = DERIVED
```

and store the derivation rule.

If self-reported:

```text
origin = SELF_REPORTED
```

If synthetic:

```text
origin = SYNTHETIC
```

with a visible UI warning:

> Synthetic demonstration signal — not a real-world indicator.

## Never use fake confidence

Do not show:

> AI confidence: 94%

unless an actual validated statistical confidence model exists and is explicitly approved.

Prefer evidence dimensions:
- source-backed
- self-reported
- derived
- missing
- synthetic
- verification required.
