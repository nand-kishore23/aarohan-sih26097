# AAROHAN — MASTER SPECIFICATION

**Version:** 1.0  
**Status:** PRODUCT CONCEPT FINAL / ENGINEERING BUILD-READY / DATA VALIDATION IN PROGRESS

## 1. Identity

**Name:** AAROHAN

**Tagline:** From Voice to Livelihood Intelligence

**Formal innovation statement:**

> Aarohan is a voice-first livelihood intelligence platform that connects individual aspirations, transferable skills, NSQF-aligned pathways and local opportunity signals with district-level PM-AJAY planning and outcome monitoring.

**Core one-line:**

> Aarohan turns beneficiary voices into personalized livelihood pathways—and turns thousands of those voices into evidence for better PM-AJAY planning.

## 2. SIH problem statement

Target problem statement:

**SIH26097 — AI-Driven voice Assistant for livelihood Mapping and NSQF-Aligned Skilling Recommendations for SC Communities under GIA component of PM-AJAY**

Sponsor:
Ministry of Social Justice and Empowerment.

Department:
Department of Social Justice and Empowerment.

Theme:
Agriculture, FoodTech & Rural Development.

The official SIH catalogue describes the need for a multilingual, voice-based conversational system that collects education, family occupation, current livelihood, skills/interests, mobility and physical constraints, employment/self-employment preference, and local economic realities; analyses skill gaps and NSQF-aligned pathways; and works through low-connectivity/low-tech channels. Source file: `SIH_2026_All_226_Problem_Statements_Master_Catalogue.pdf`.

## 3. Problem interpretation

The problem is not simply course discovery.

The core difficulty is that beneficiary capability and aspirations can be informal, conversational, multilingual, and poorly represented by text-heavy systems.

Aarohan therefore begins with:

```text
Voice
 ↓
Conversation
 ↓
Structured profile
 ↓
Informal experience
 ↓
Transferable skills
 ↓
Formal qualification/pathway evidence
```

The system then combines:
- beneficiary information,
- verified qualification information,
- access constraints,
- training capacity,
- opportunity evidence where available.

## 4. Product boundary

Aarohan IS:
- a voice-first livelihood intelligence layer,
- a beneficiary profiling and skill-extraction system,
- an explainable pathway decision-support system,
- a district-level aggregation/evidence system,
- an AI-assisted evidence-brief generator.

Aarohan IS NOT:
- PM-AJAY MIS,
- an autonomous government decision-maker,
- a qualification authority,
- a training-provider marketplace,
- an employment prediction engine,
- a vacancy guarantee system,
- a budget approval engine,
- a replacement for NSDC/NSQF/Skill India/NCS,
- a claim of live government integration unless such integration is actually implemented and authorized.

## 5. Frozen core pipeline

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

## 6. Person layer

```text
Voice
 ↓
Conversation
 ↓
Profile
 ↓
Informal experience
 ↓
Transferable skills
 ↓
Candidate pathways (0–3)
 ↓
Skill gaps
 ↓
Access constraints
 ↓
Evidence
 ↓
Why this
Why not
What could prevent it
 ↓
Human decision
```

The system must never force exactly three pathways.

Rules:
- 0 valid candidates -> explain insufficient evidence / no supported candidate.
- 1 valid candidate -> show 1.
- 2 valid candidates -> show 2.
- 3+ valid candidates -> show at most 3.

Candidate pathways are deterministic outputs from the canonical pathway catalogue plus profile evidence. LLMs do not invent candidate qualifications.

## 7. Government/community layer

```text
Many beneficiary profiles
 ↓
Anonymized aggregation
 ↓
Observed beneficiary interest
 ↓
Training capacity
 ↓
Opportunity evidence
 ↓
Potential interest-capacity mismatch
 ↓
Livelihood Evidence Brief
 ↓
Human review
```

Use:
- **Observed beneficiary interest**, not guaranteed demand.
- **Potential interest-capacity mismatch**, not guaranteed demand shortage.

Changing training capacity must change the derived mismatch result.

## 8. Evidence Brief

Primary government-facing analytical output:

```text
DISTRICT / AREA
Data period

Beneficiary profiles represented
Observed interest
Training capacity
Potential mismatch
Opportunity evidence
Evidence gaps
Suggested next validation
```

Required label:

> AI-assisted analytical brief — human review required

The brief supports planning; it does not create, approve, or replace an official PM-AJAY Perspective Plan.

## 9. Qualification/livelihood object model

Do not collapse these concepts:

```text
Pathway
 ↓
Occupation
 ↓
Qualification
 ↓
QP
 ↓
NSQF
 ↓
NOS
 ↓
Competencies / skills
```

An informal statement such as:

> "I repair tractors"

must not be directly mapped from natural language to a QP.

Instead:

```text
raw experience
 ↓
normalized skill(s)
 ↓
candidate occupation/pathway
 ↓
verified qualification
 ↓
NOS / competencies
 ↓
skill gap
```

## 10. Current pathway candidates

These are candidates pending final competency-level audit.

### Candidate A

**Tractor Mechanic**
- QP code: `AGR/Q1108`
- NSQF level: 4
- Sector council: Agriculture Skill Council of India
- Occupation: Farm Machinery, Equipment Operation and Maintenance
- Current NSDC public export lists the record as National Occupational Standards.
- NSDC content availability shows multiple records/variants under the same QP code, including Tractor Mechanic, Tractor Mechanic_v2, and Tractor Service Mechanic.

**Engineering consequence:** `record_variant` / version must be retained. QP code alone is not a complete identity.

### Candidate B

**Multi Skill Technician (Electrical)**
- QP code: `ELE/Q3115`
- NSQF level: 4
- Sector council: Electronics Sector Skills Council of India
- Occupation: After Sales Service
- NSDC page identifies the QP as Occupational Standards and gives validation date 02-03-2021.

### Candidate C

**Dairy Product Processor**
- QP code: `QG-04-FI-02933-2024-V2-FICSI`
- NSQF level: 4
- Awarding body: Food Industry Capacity & Skill Initiative (FICSI)
- QP-NOS booklet lists 900 total notional hours.
- NQR qualification file identifies approval in the 39th NSQC meeting dated 27 Aug 2024.
- NQR qualification file contains NOS/module structure and assessment information.

**Status:** candidate data is strong enough to audit, but canonical catalogue is not FINAL until the complete source record is extracted and validated.

## 11. Pathways deliberately excluded/held

- Generic "Food Processing": rejected as too broad; use a specific qualification.
- "Digital Services": dropped as an MVP umbrella pathway.
- Sewing Machine Operator (`AMH/Q0301`): held pending current authoritative status/version reconciliation.
- Agriculture Machinery Repair and Maintenance Service Provider (`AGR/Q1111`): do not use; the NSDC export identifies it as Retired Occupational Standards.
- Agriculture Machinery Operator (`AGR/Q1103`): do not use; NSDC export identifies it as Retired Occupational Standards.
- Self Employed Tailor (`AMH/Q1947`): held/rejected because the prior audit identified it as retired.

## 12. AI boundary

### LLM responsibilities

- speech/transcript interpretation
- conversational interview
- adaptive clarification
- extraction of raw experience
- natural-language skill normalization assistance
- explanation of deterministic results
- voice response generation.

### Deterministic responsibilities

- qualification retrieval
- qualification status/version validation
- eligibility/rules
- skill matching
- skill-gap calculation
- access/constraint filtering
- training capacity calculations
- opportunity evidence status
- district aggregation
- mismatch calculation
- candidate pathway filtering/ranking
- provenance.

LLM output must be treated as structured input to deterministic validation, not as authority.

## 13. Provenance labels

Every important data item uses:

- `SOURCE_BACKED`
- `SELF_REPORTED`
- `DERIVED`
- `SYNTHETIC`
- `MISSING`

UI labels:

- 🟢 Source-backed
- 🔵 Self-reported
- 🟣 Derived
- 🟠 Synthetic
- ⚪ Missing

## 14. Evidence model

Every important claim should support:

```text
CLAIM
 ↓
SOURCE
 ↓
EVIDENCE / VERIFICATION STATUS
 ↓
LAST UPDATED
```

Opportunity evidence additionally records:
- source
- source type
- source URL/reference
- geography
- published date
- retrieved at
- valid from
- valid until
- coverage
- status.

If evidence is insufficient:

> OPPORTUNITY EVIDENCE INSUFFICIENT — Field validation required.

No employment prediction or guarantee.

## 15. Stress test

The stress test is a view over existing pathway data, not a separate AI subsystem.

It checks how a pathway is affected by:
- low training availability,
- distance/access constraint,
- weak opportunity evidence,
- skill gap,
- missing evidence.

It does not predict employment.

## 16. MVP interfaces

### Beneficiary

1. Voice Interview
2. Profile
3. Candidate Pathways (0–3)
4. Stress Test / Why / Why Not

### Officer

5. Demand / Community Dashboard
6. Capacity Mismatch
7. Evidence Brief

No giant GIS and no unnecessary dashboard suite.

## 17. MVP scale

Use approximately **500 synthetic beneficiary profiles** for demonstration.

Aggregation must be real code.

Example:

```text
500 synthetic profiles
 ↓
normalize skills/interests
 ↓
group by pathway
 ↓
observed interest count
 ↓
compare with training capacity
 ↓
potential mismatch
```

Do not use fake "10,000 real beneficiaries".

## 18. Synthetic data rules

Synthetic opportunity signals and beneficiaries must be explicitly labelled.

Example:

> Synthetic demonstration signal — not a real-world employment indicator.

No fabricated 30/60/90-day outcomes.

## 19. Opportunity data boundary

The MVP must not claim a live NCS API or live labour-market feed unless actually integrated through an authorized, working interface.

Possible future integrations may include NCS, Skill India, PM-AJAY MIS, or other official sources, but they are not MVP dependencies.

## 20. Low-connectivity boundary

The problem statement calls for IVR, WhatsApp voice notes, and lightweight mobile/kiosk approaches.

MVP:
- primary: web/PWA voice interaction.
- architecture-ready: channel adapters.
- no claim of production IVR or WhatsApp integration unless actually implemented.

## 21. Security/privacy

- Do not expose identifiable beneficiary records in district aggregation.
- Separate raw voice/transcript from derived profile data.
- Store provenance for extracted information.
- Minimize logging of raw voice.
- Use environment variables for secrets.
- Do not hard-code API keys.
- Do not use production personal data in the demo.

## 22. Non-goals

Do not build:
- blockchain
- generic chatbot
- AI-generated business plans
- automatic government budgets
- provider ranking
- live government integrations without authorization
- employment probability prediction
- fabricated opportunity scores
- giant GIS
- production WhatsApp
- production IVR
- automatic PM-AJAY plan generation/approval.

## 23. Build gate

Before database schema lock:

```text
AGR/Q1108
ELE/Q3115
Dairy Product Processor
        ↓
complete source extraction
        ↓
NOS / competency validation
        ↓
canonical catalogue
        ↓
matching rules
        ↓
database schema
```

Do not skip this order.
