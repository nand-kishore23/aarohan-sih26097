# DATA AUDIT

## Audit gate

This document is a living audit record. The qualification catalogue is not FINAL until every candidate has complete source extraction and validation.

## Current candidates

| Candidate | QP | NSQF | Current status |
|---|---|---:|---|
| Tractor Mechanic | AGR/Q1108 | 4 | Candidate; version/record reconciliation required |
| Multi Skill Technician (Electrical) | ELE/Q3115 | 4 | Candidate; source record identified |
| Dairy Product Processor | QG-04-FI-02933-2024-V2-FICSI | 4 | Candidate; NQR source identified |

## Tractor Mechanic

Authoritative source observations:
- NSDC export lists AGR/Q1108.
- Occupational area: Farm Machinery, Equipment Operation and Maintenance.
- QP name: Tractor Mechanic.
- NSQF Level 4.
- Source PDF: `https://nsdcindia.org/sites/default/files/AGRQ1108_Tractor%20Mechanic_v1_28.05.2018.pdf`
- NSDC content availability shows multiple records for AGR/Q1108:
  - Tractor Mechanic
  - Tractor Mechanic_v2
  - Tractor Service Mechanic

### Required before lock

- identify exact record/version intended for MVP.
- extract all NOS.
- extract NOS codes and versions.
- extract competencies/performance criteria.
- extract knowledge requirements.
- extract tools/equipment.
- extract training hours.
- extract eligibility.
- extract assessment information.
- validate current status for selected record.

## Multi Skill Technician (Electrical)

Authoritative source observations:
- NSDC page: Multi Skill Technician (Electrical).
- QP code: ELE/Q3115.
- NSQF Level 4.
- Sector council: Electronics Sector Skills Council of India.
- Occupation: After Sales Service.
- QP file: `ELE_Q3115_Multi_Skill_Technician_(Electrical)_v1.0_2-3-2021.pdf`
- Model curriculum listed.
- Validated on 02-03-2021.
- NSDC public export/content listing identifies it as National Occupational Standards / Occupational Standards.

### Required before lock

- extract complete NOS list.
- extract NOS codes/versions.
- extract competencies/performance criteria.
- extract knowledge requirements.
- extract tools/equipment.
- extract training hours.
- extract eligibility.
- extract assessment.
- validate current status and record variant.

## Dairy Product Processor

Authoritative source observations:
- NQR qualification file exists for `QG-04-FI-02933-2024-V2-FICSI`.
- Approved in 39th NSQC meeting dated 27 Aug 2024.
- NQR version reported as 3.0.
- Reference code: QG-04-FI-02933-2024-V2-FICSI.
- NSDC QP-NOS booklet lists:
  - Dairy Product Processor
  - Level 4
  - 900 hours
  - awarding body FICSI.
- NQR source contains mandatory/elective NOS/module structure and assessment information.

### Required before lock

- extract all mandatory NOS.
- extract all elective NOS and selection rules.
- extract NOS codes/versions.
- extract competencies/performance criteria.
- extract knowledge requirements.
- extract training hours.
- extract eligibility.
- extract assessment.
- reconcile NQR version with booklet naming/version.

## Rejected/held evidence

### AGR/Q1111
NSDC export marks Agriculture Machinery Repair and Maintenance Service Provider as Retired Occupational Standards.
Do not use.

### AGR/Q1103
NSDC export marks Agriculture Machinery Operator as Retired Occupational Standards.
Do not use.

### AMH/Q1947
Previously audited as retired; do not use unless a future authoritative current record proves otherwise.

### AMH/Q0301
Hold pending current record/version reconciliation.

## Audit principle

Never mark a qualification `validated` merely because a search result exists.

`validated` means:
- source identified,
- record identity resolved,
- status resolved,
- competency/NOS data extracted,
- provenance captured,
- canonical JSON generated,
- validation checks pass.
