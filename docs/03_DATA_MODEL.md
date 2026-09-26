# DATA MODEL

This document describes the intended data model. Production schema is NOT locked until qualification catalogue validation is complete.

## Qualification domain

### qualification

- id
- qp_code
- qp_name
- display_name
- record_variant
- version
- status
- nsqf_level
- sector_council
- occupational_area
- source_id
- source_url
- source_published_at
- retrieved_at
- valid_from
- valid_until
- validation_notes

### qualification_nos

- id
- qualification_id
- nos_code
- nos_name
- version
- core_or_elective
- source_reference

### competency

- id
- qualification_nos_id
- competency_code
- competency_name
- competency_type
- description
- source_reference

### qualification_eligibility

- id
- qualification_id
- requirement_type
- requirement_value
- source_reference

### qualification_training

- id
- qualification_id
- theory_hours
- practical_hours
- ojt_hours
- total_hours
- source_reference

### qualification_assessment

- id
- qualification_id
- assessment_component
- marks
- weightage
- source_reference

## Beneficiary domain

### beneficiary

- id
- district_id
- age_group
- education_level
- preferred_language
- current_livelihood
- employment_preference
- mobility_radius_km
- physical_constraint
- created_at
- data_origin

### voice_session

- id
- beneficiary_id
- language
- started_at
- ended_at
- transcript_reference
- retention_status
- data_origin

### skill_observation

- id
- beneficiary_id
- raw_skill
- normalized_skill_id
- evidence_text
- source_type
- verification_status
- created_at

### skill

- id
- canonical_name
- aliases
- skill_domain

### interest

- id
- beneficiary_id
- normalized_interest
- pathway_domain
- source_type

## Training capacity

### training_capacity

- id
- district_id
- qualification_id
- provider_name
- available_seats
- delivery_mode
- period_start
- period_end
- source_reference
- data_origin
- provenance_status

## Opportunity evidence

### opportunity_signal

- id
- pathway_id
- district_id
- signal_type
- signal_value
- source_name
- source_type
- source_reference
- geography
- published_date
- retrieved_at
- valid_from
- valid_until
- coverage
- status
- data_origin

## Derived community data

### derived_district_signal

- district_id
- pathway_id
- period
- observed_interest_count
- training_capacity
- interest_capacity_gap
- mismatch_status
- calculation_version
- generated_at
- data_origin = DERIVED

## Candidate pathway

### candidate_pathway

- id
- beneficiary_id
- pathway_id
- generated_at
- supporting_evidence
- skill_gaps
- constraints
- exclusion_reasons
- evidence_status
- decision_status

Do not add fields merely because a future idea might need them.
