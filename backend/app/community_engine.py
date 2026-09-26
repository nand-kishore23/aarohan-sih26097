"""Community Intelligence Data Generator and Aggregation Engine."""

import random
from collections import defaultdict
from typing import List, Dict
import uuid

from .models import (
    Beneficiary, TrainingCapacity, OpportunitySignal,
    PathwayAggregation, CommunitySummary, EvidenceBrief,
    ProvenanceOrigin, Qualification
)
from .seed_data import QUALIFICATION_CATALOGUE

# Fixed seed for deterministic synthetic data generation
random.seed(42)

DISTRICT = "Demo District"
DATA_PERIOD = "Q3 2026 (Synthetic)"

# Generate 500 Synthetic Beneficiaries
def generate_synthetic_beneficiaries(count: int = 500) -> List[Beneficiary]:
    beneficiaries = []
    
    # We map interests directly to qualification IDs for simplified prototype simulation
    qual_ids = list(QUALIFICATION_CATALOGUE.keys())
    
    for i in range(count):
        # Deterministically assign interests to simulate a specific distribution
        # e.g., 50% Tractor, 30% Electrical, 20% Dairy
        rand_val = random.random()
        if rand_val < 0.5:
            qual_id = "AGR-Q1108"
            interests = ["tractor repair", "farm machinery"]
            livelihood = "Farm helper"
        elif rand_val < 0.8:
            qual_id = "ELE-Q3115"
            interests = ["electrical work", "appliance repair"]
            livelihood = "Apprentice electrician"
        else:
            qual_id = "QG-04-FI-02933"
            interests = ["dairy processing", "food handling"]
            livelihood = "Dairy farm worker"
            
        ben = Beneficiary(
            id=f"synth-{i}",
            name=f"Synthetic Beneficiary {i}",
            age_group=random.choice(["18-25", "25-35", "35-45"]),
            education=random.choice(["8th Pass", "10th Pass", "12th Pass"]),
            district=DISTRICT,
            preferred_language="Hindi",
            current_livelihood=livelihood,
            work_experience="Informal",
            employment_preference="employment",
            mobility_radius_km=random.choice([10, 20, 50]),
            data_origin=ProvenanceOrigin.SYNTHETIC,
            skills=[],  # Not using detailed skills for this macro aggregation in prototype
            interests=interests,
            raw_statement="Synthetic record",
        )
        
        # In the real system, interest is mapped to pathway via the engine. 
        # For the prototype community aggregation, we'll store the 'intended pathway' as a custom field 
        # or infer it from the interest array during aggregation.
        # Let's attach it dynamically so the aggregator knows which pathway this person represents.
        ben.pathway_interest = qual_id 
        
        beneficiaries.append(ben)
        
    return beneficiaries


def generate_training_capacity() -> List[TrainingCapacity]:
    # We hardcode some capacities to create interesting mismatches
    return [
        TrainingCapacity(
            id="cap-1",
            district=DISTRICT,
            pathway_id="AGR-Q1108", # Using Qual ID as pathway ID for prototype simplicity
            qualification_id="AGR-Q1108",
            provider_name="Demo Agri Skills Center",
            available_seats=50,  # High interest (250), low capacity (50) -> Shortage
            period_start="2026-09-01",
            period_end="2026-12-31"
        ),
        TrainingCapacity(
            id="cap-2",
            district=DISTRICT,
            pathway_id="ELE-Q3115",
            qualification_id="ELE-Q3115",
            provider_name="Regional Electronics Training Inst.",
            available_seats=200, # Med interest (150), high capacity (200) -> Surplus
            period_start="2026-09-01",
            period_end="2026-12-31"
        ),
        TrainingCapacity(
            id="cap-3",
            district=DISTRICT,
            pathway_id="QG-04-FI-02933",
            qualification_id="QG-04-FI-02933",
            provider_name="Dairy Co-op Training",
            available_seats=100, # Low interest (100), balanced capacity (100) -> Balanced
            period_start="2026-09-01",
            period_end="2026-12-31"
        )
    ]

def generate_opportunity_signals() -> List[OpportunitySignal]:
    return [
        OpportunitySignal(
            id="opp-1",
            pathway_id="AGR-Q1108",
            district=DISTRICT,
            signal_type="Job Postings",
            signal_value="High Demand (Synthetic)",
            source_name="Synthetic Job Board",
            source_reference="Ref-1",
            published_date="2026-09-01",
            retrieved_at="2026-09-25",
            coverage="District wide",
            status="ACTIVE"
        ),
        OpportunitySignal(
            id="opp-2",
            pathway_id="ELE-Q3115",
            district=DISTRICT,
            signal_type="Employer Survey",
            signal_value="Moderate Demand",
            source_name="Synthetic Industry Survey",
            source_reference="Ref-2",
            published_date="2026-09-01",
            retrieved_at="2026-09-25",
            coverage="Regional",
            status="ACTIVE"
        )
        # Missing evidence for Dairy
    ]

# Initialize data
synthetic_beneficiaries = generate_synthetic_beneficiaries(500)
synthetic_capacity = generate_training_capacity()
synthetic_opportunity = generate_opportunity_signals()

# ── Aggregation Engine ────────────────────────────────────────────────

def aggregate_community_intelligence() -> CommunitySummary:
    """Calculates observed interest, capacity, and mismatches dynamically."""
    
    # 1. Count observed interest per pathway
    interest_counts = defaultdict(int)
    for ben in synthetic_beneficiaries:
        # In prototype, we assigned pathway_interest directly
        if hasattr(ben, 'pathway_interest'):
            interest_counts[ben.pathway_interest] += 1
            
    # 2. Sum training capacity per pathway
    capacity_sums = defaultdict(int)
    for cap in synthetic_capacity:
        capacity_sums[cap.pathway_id] += cap.available_seats
        
    # 3. Get opportunity evidence status
    opp_status = defaultdict(lambda: "OPPORTUNITY EVIDENCE INSUFFICIENT")
    for opp in synthetic_opportunity:
        opp_status[opp.pathway_id] = "EVIDENCE AVAILABLE"
        
    # 4. Build aggregations
    pathway_aggs = []
    for qual_id, qual in QUALIFICATION_CATALOGUE.items():
        interest = interest_counts[qual_id]
        capacity = capacity_sums[qual_id]
        gap = interest - capacity
        
        if gap > 20:
            mismatch = "Capacity Shortfall"
        elif gap < -20:
            mismatch = "Excess Capacity"
        else:
            mismatch = "Balanced"
            
        agg = PathwayAggregation(
            pathway_id=qual_id,
            qualification_id=qual_id,
            pathway_name=qual.display_name or qual.name,
            observed_interest_count=interest,
            training_capacity=capacity,
            interest_capacity_gap=gap,
            mismatch_status=mismatch,
            opportunity_evidence_status=opp_status[qual_id]
        )
        pathway_aggs.append(agg)
        
    return CommunitySummary(
        district=DISTRICT,
        data_period=DATA_PERIOD,
        beneficiaries_represented=len(synthetic_beneficiaries),
        pathways=pathway_aggs
    )

def generate_evidence_brief() -> EvidenceBrief:
    """Generates the analytical brief based on the aggregations."""
    summary = aggregate_community_intelligence()
    
    # Analyze the overall picture
    total_interest = sum(p.observed_interest_count for p in summary.pathways)
    total_capacity = sum(p.training_capacity for p in summary.pathways)
    
    shortfalls = [p for p in summary.pathways if p.interest_capacity_gap > 0]
    
    interest_str = f"Strongest observed interest is in {summary.pathways[0].pathway_name}."
    cap_str = f"Total training capacity across analyzed pathways is {total_capacity} seats."
    
    if shortfalls:
        mismatch_str = f"Significant capacity shortfall detected in {shortfalls[0].pathway_name} (Gap: {shortfalls[0].interest_capacity_gap} seats)."
    else:
        mismatch_str = "Training capacity appears adequate for observed interest."
        
    missing_evidence = [p.pathway_name for p in summary.pathways if p.opportunity_evidence_status == "OPPORTUNITY EVIDENCE INSUFFICIENT"]
    
    return EvidenceBrief(
        district=DISTRICT,
        data_period=DATA_PERIOD,
        beneficiaries_represented=len(synthetic_beneficiaries),
        observed_interest_summary=interest_str,
        training_capacity_summary=cap_str,
        potential_mismatch_summary=mismatch_str,
        opportunity_evidence_status="Partial coverage" if missing_evidence else "Adequate coverage",
        evidence_gaps=[
            f"Missing field opportunity evidence for: {', '.join(missing_evidence)}" if missing_evidence else "No major evidence gaps."
        ],
        suggested_next_validation=[
            "Conduct field survey to validate employer demand in unsupported pathways.",
            "Verify actual enrollment rates vs available capacity."
        ]
    )
