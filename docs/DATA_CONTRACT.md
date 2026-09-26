# DATA CONTRACT

## Universal record shape

Every material fact should conceptually carry:

```json
{
  "value": null,
  "provenance": {
    "origin": "MISSING",
    "source_name": null,
    "source_type": null,
    "source_reference": null,
    "source_url": null,
    "published_date": null,
    "retrieved_at": null,
    "valid_from": null,
    "valid_until": null,
    "verification_status": "MISSING"
  }
}
```

## Allowed origin values

```text
SOURCE_BACKED
SELF_REPORTED
DERIVED
SYNTHETIC
MISSING
```

## Canonical qualification requirements

At minimum:

```text
qualification_id
qp_code
name
record_variant
version
status
nsqf_level
source
nos[]
competencies[]
eligibility[]
training
assessment
```

Unknown subfields remain null/missing until validated.

## Qualification source rule

A qualification may enter the deterministic engine only if:
- identity resolved,
- source identified,
- status resolved,
- required competency data extracted,
- validation passed.

## Derived record requirements

Derived records include:
- calculation rule
- input references
- calculation version
- generated timestamp.

## Synthetic record requirements

Synthetic records include:
- scenario ID
- generation version
- synthetic flag.

## Self-reported record requirements

Self-reported records include:
- beneficiary/session reference
- evidence text/reference
- verification status.

## Never use

```json
{
  "value": "estimated"
}
```

unless estimation is explicitly part of an approved model.

Prefer:

```json
{
  "value": null,
  "provenance": {
    "origin": "MISSING"
  }
}
```
