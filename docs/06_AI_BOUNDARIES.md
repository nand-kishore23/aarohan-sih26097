# AI BOUNDARIES

## LLM owns

### Conversation
Natural-language interview and adaptive questions.

### Extraction
Turn beneficiary statements into structured candidate facts.

### Clarification
Ask follow-up questions when required fields are missing.

### Normalization assistance
Suggest possible canonical skill labels for deterministic validation.

### Explanation
Explain deterministic engine outputs in accessible language.

## LLM does not own

- QP creation
- NOS creation
- NSQF assignment
- qualification status
- eligibility rules
- competency definitions
- pathway generation outside the canonical catalogue
- market demand calculation
- training capacity calculation
- district aggregation
- government decisions.

## Guardrail pattern

```text
LLM output
 ↓
JSON schema validation
 ↓
provenance assignment
 ↓
deterministic validation
 ↓
canonical storage
```

## Hallucination policy

When source data is absent:

```text
UNKNOWN
```

When the LLM cannot safely normalize:

```text
UNRESOLVED_SKILL
```

Do not guess.

## Voice pipeline

Architecture may be:

```text
audio
 ↓
ASR
 ↓
language detection where supported
 ↓
LLM conversation/extraction
 ↓
deterministic backend
 ↓
response text
 ↓
translation/TTS where actually implemented
```

Do not claim multilingual coverage that has not been tested.
