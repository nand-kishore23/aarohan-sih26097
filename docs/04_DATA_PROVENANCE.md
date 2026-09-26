# DATA PROVENANCE

## Origin types

| Origin | Meaning |
|---|---|
| SOURCE_BACKED | Directly supported by an authoritative/public source |
| SELF_REPORTED | Supplied by beneficiary/user |
| DERIVED | Calculated by Aarohan from stored data |
| SYNTHETIC | Demo-generated |
| MISSING | No reliable evidence |

## Verification statuses

Use explicit statuses such as:
- VERIFIED
- REQUIRES_VERIFICATION
- UNVERIFIED
- CONFLICTING
- MISSING

## Required provenance fields

For source-backed facts:

```text
source_name
source_type
source_reference
source_url
published_date
retrieved_at
valid_from
valid_until
verification_status
```

For self-reported facts:

```text
source_type = BENEFICIARY_INTERVIEW
origin = SELF_REPORTED
evidence_reference = voice_session/transcript
verification_status = UNVERIFIED
```

For derived facts:

```text
origin = DERIVED
calculation_rule
input_references
calculation_version
generated_at
```

For synthetic facts:

```text
origin = SYNTHETIC
scenario_id
generation_version
```

## Evidence display

Use provenance badges in every important UI location.

## Unknown handling

Never transform:
- missing evidence into low confidence,
- self-reported evidence into verified evidence,
- synthetic opportunity data into market evidence.

## Claim model

```text
CLAIM
 ↓
SOURCE
 ↓
EVIDENCE STATUS
 ↓
VERIFICATION STATUS
 ↓
LAST UPDATED
```

## Opportunity evidence

If no adequate opportunity source exists:

```text
status = INSUFFICIENT
```

Display:

> Opportunity evidence insufficient — field validation required.

Never display a fabricated market score.
