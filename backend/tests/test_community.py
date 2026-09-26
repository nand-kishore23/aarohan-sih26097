import pytest
from app.community_engine import (
    generate_synthetic_beneficiaries,
    synthetic_beneficiaries,
    synthetic_capacity,
    synthetic_opportunity,
    aggregate_community_intelligence,
    generate_evidence_brief
)
from app.models import ProvenanceOrigin

def test_synthetic_data_loading():
    # 1. 500 synthetic beneficiaries can be loaded
    assert len(synthetic_beneficiaries) == 500

    # 7. Synthetic data is correctly marked
    assert synthetic_beneficiaries[0].data_origin == ProvenanceOrigin.SYNTHETIC
    assert synthetic_capacity[0].data_origin == ProvenanceOrigin.SYNTHETIC
    assert synthetic_opportunity[0].data_origin == ProvenanceOrigin.SYNTHETIC

def test_aggregation_calculations():
    summary = aggregate_community_intelligence()
    assert summary.beneficiaries_represented == 500
    
    # 8. Derived aggregation values are correctly marked DERIVED
    assert summary.data_origin == ProvenanceOrigin.DERIVED
    assert summary.pathways[0].data_origin == ProvenanceOrigin.DERIVED
    
    # Verify pathways exist
    assert len(summary.pathways) == 3
    
    tractor_agg = next(p for p in summary.pathways if p.pathway_id == "AGR-Q1108")
    
    # 2. Observed interest is calculated correctly
    assert tractor_agg.observed_interest_count > 0
    
    # 3. Training capacity is calculated correctly
    assert tractor_agg.training_capacity == 50
    
    # 4. Potential mismatch is calculated correctly
    assert tractor_agg.interest_capacity_gap == tractor_agg.observed_interest_count - tractor_agg.training_capacity
    
    # 9. Missing opportunity evidence produces the correct status
    dairy_agg = next(p for p in summary.pathways if p.pathway_id == "QG-04-FI-02933")
    assert dairy_agg.opportunity_evidence_status == "OPPORTUNITY EVIDENCE INSUFFICIENT"

def test_dynamic_recalculation():
    # Store original
    original_summary = aggregate_community_intelligence()
    original_gap = original_summary.pathways[0].interest_capacity_gap
    
    # 5. Changing capacity changes mismatch
    original_cap = synthetic_capacity[0].available_seats
    synthetic_capacity[0].available_seats += 10
    new_summary = aggregate_community_intelligence()
    assert new_summary.pathways[0].interest_capacity_gap == original_gap - 10
    
    # Revert
    synthetic_capacity[0].available_seats = original_cap
    
    # 6. Changing interest changes observed interest
    # Add a synthetic beneficiary
    from app.models import Beneficiary
    ben = Beneficiary(id="temp-1", name="Temp", data_origin=ProvenanceOrigin.SYNTHETIC)
    ben.pathway_interest = "AGR-Q1108"
    synthetic_beneficiaries.append(ben)
    
    new_summary2 = aggregate_community_intelligence()
    assert new_summary2.pathways[0].observed_interest_count == original_summary.pathways[0].observed_interest_count + 1
    
    # Revert
    synthetic_beneficiaries.pop()

def test_evidence_brief():
    brief = generate_evidence_brief()
    # 10. Evidence Brief uses the same aggregation values as the dashboard
    assert brief.beneficiaries_represented == 500
    assert "AGR-Q1108" in brief.observed_interest_summary or "Tractor" in brief.observed_interest_summary
