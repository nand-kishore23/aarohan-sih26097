"""Prototype seed data for AAROHAN SIH 2026 demo.

All qualification NOS/competencies are marked PARTIALLY_VERIFIED.
All beneficiary data is marked SYNTHETIC.
"""
from .models import (
    Beneficiary, Competency, CandidatePathway, Provenance,
    ProvenanceOrigin, Qualification, QualificationNOS,
    QualificationTraining, SkillObservation, VerificationStatus,
)

_PROTO_PROV = Provenance(
    origin=ProvenanceOrigin.SOURCE_BACKED,
    source_name="NSDC / Sector Skill Council",
    verification_status=VerificationStatus.PARTIALLY_VERIFIED,
    retrieved_at="2026-09-25",
)

# ══════════════════════════════════════════════════════════════════════
# 1.  AGR/Q1108 — Tractor Service Mechanic
# ══════════════════════════════════════════════════════════════════════
QUAL_TRACTOR = Qualification(
    id="AGR-Q1108",
    qp_code="AGR/Q1108",
    name="Tractor Service Mechanic",
    display_name="Tractor Service Mechanic",
    version="3.0",
    status="PROTOTYPE",
    nsqf_level=4,
    sector_council="Agriculture Skill Council of India (ASCI)",
    occupational_area="Farm Machinery, Equipment Operation and Maintenance",
    eligibility=["10th pass or equivalent", "Minimum age 18"],
    training=QualificationTraining(
        theory_hours=120, practical_hours=200, ojt_hours=70, total_hours=390
    ),
    provenance=Provenance(
        origin=ProvenanceOrigin.SOURCE_BACKED,
        source_name="ASCI / NSDC",
        source_url="https://nsdcindia.org/tractor-service-mechanic",
        verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        retrieved_at="2026-09-25",
    ),
    required_skills=[
        "tractor_repair", "engine_repair", "mechanical_troubleshooting",
        "farm_machinery_maintenance", "pump_repair", "hydraulic_systems",
        "electrical_systems", "transmission_systems", "safety_procedures",
    ],
    nos=[
        QualificationNOS(
            code="AGR/N1108-1", name="Engine Systems Maintenance",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC1", name="Inspect and diagnose engine faults",
                           description="Identify engine problems through visual inspection, sound, and diagnostic tools"),
                Competency(code="PC2", name="Service IC engine components",
                           description="Service and maintain cooling, lubrication, air and exhaust systems"),
                Competency(code="PC3", name="Perform engine overhaul",
                           description="Disassemble, repair, and reassemble engine parts per specifications"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="AGR/N1108-2", name="Transmission & Hydraulic Systems",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC4", name="Service clutch and gearbox",
                           description="Inspect, adjust and repair clutch assemblies and gearbox systems"),
                Competency(code="PC5", name="Maintain hydraulic systems",
                           description="Service hydraulic pumps, cylinders, valves and connections"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="AGR/N1108-3", name="Auto-Electrical Systems",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC6", name="Service electrical systems",
                           description="Test and repair starting motor, alternator, battery and wiring"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="AGR/N1108-4", name="Safety & Workshop Practices",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC7", name="Follow safety procedures",
                           description="Use PPE, maintain clean workspace, follow SOP for hazardous materials"),
                Competency(code="PC8", name="Use tools and equipment correctly",
                           description="Select, use and maintain workshop tools and measuring instruments"),
            ],
            provenance=_PROTO_PROV,
        ),
    ],
)

# ══════════════════════════════════════════════════════════════════════
# 2.  ELE/Q3115 — Multi Skill Technician (Electrical)
# ══════════════════════════════════════════════════════════════════════
QUAL_ELECTRICAL = Qualification(
    id="ELE-Q3115",
    qp_code="ELE/Q3115",
    name="Multi Skill Technician (Electrical)",
    display_name="Multi Skill Technician (Home Appliances)",
    version="2.0",
    status="PROTOTYPE",
    nsqf_level=4,
    sector_council="Electronics Sector Skills Council of India (ESSCI)",
    occupational_area="After Sales Service — Home Appliances",
    eligibility=["10th pass or equivalent", "Minimum age 18"],
    training=QualificationTraining(
        theory_hours=100, practical_hours=180, ojt_hours=60, total_hours=340
    ),
    provenance=Provenance(
        origin=ProvenanceOrigin.SOURCE_BACKED,
        source_name="ESSCI / NSDC",
        source_url="https://nsdcindia.org/node/33121",
        verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        retrieved_at="2026-09-25",
    ),
    required_skills=[
        "electrical_repair", "wiring", "appliance_repair",
        "motor_repair", "led_repair", "soldering",
        "customer_service", "safety_procedures",
    ],
    nos=[
        QualificationNOS(
            code="ELE/N3115-1", name="LED/CFL Lighting Systems Repair",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC1", name="Diagnose lighting faults",
                           description="Test and identify faults in LED, CFL and conventional lighting"),
                Competency(code="PC2", name="Replace and repair components",
                           description="Replace drivers, ballasts and wiring in lighting systems"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="ELE/N3115-2", name="Heating Appliance Repair",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC3", name="Service geysers and water heaters",
                           description="Diagnose and repair heating elements, thermostats and safety valves"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="ELE/N3115-3", name="Motor-driven Appliance Repair",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC4", name="Service fans and motors",
                           description="Diagnose and repair ceiling fans, table fans and small motors"),
                Competency(code="PC5", name="Service mixer-grinders",
                           description="Repair motor, couplers and speed control in mixer-grinder units"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="ELE/N3115-4", name="Safety, Tools & Customer Service",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC6", name="Follow electrical safety procedures",
                           description="Use PPE, follow lockout-tagout, handle live circuits safely"),
                Competency(code="PC7", name="Communicate with customers",
                           description="Explain faults, provide cost estimates, maintain service records"),
            ],
            provenance=_PROTO_PROV,
        ),
    ],
)

# ══════════════════════════════════════════════════════════════════════
# 3.  Dairy Product Processor
# ══════════════════════════════════════════════════════════════════════
QUAL_DAIRY = Qualification(
    id="QG-04-FI-02933",
    qp_code="QG-04-FI-02933-2024-V2-FICSI",
    name="Dairy Product Processor",
    display_name="Dairy Product Processor",
    version="V2-FICSI",
    status="PROTOTYPE",
    nsqf_level=4,
    sector_council="Food Industry Capacity & Skill Initiative (FICSI)",
    occupational_area="Dairy Products Processing",
    eligibility=["12th pass (no experience) or 10th pass with 2 years experience", "Minimum age 18"],
    training=QualificationTraining(
        theory_hours=90, practical_hours=180, ojt_hours=60, total_hours=900
    ),
    provenance=Provenance(
        origin=ProvenanceOrigin.SOURCE_BACKED,
        source_name="NQR / FICSI",
        source_url="https://www.nqr.gov.in",
        verification_status=VerificationStatus.PARTIALLY_VERIFIED,
        retrieved_at="2026-09-25",
    ),
    required_skills=[
        "dairy_processing", "milk_testing", "pasteurization",
        "quality_control", "food_safety", "equipment_operation",
        "record_keeping", "hygiene_procedures",
    ],
    nos=[
        QualificationNOS(
            code="FIC/N9026", name="Prepare for Production",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC1", name="Prepare workspace and equipment",
                           description="Sanitize work area, check equipment readiness, gather raw materials"),
                Competency(code="PC2", name="Receive and test milk",
                           description="Conduct fat, SNF, acidity, adulteration tests on incoming milk"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="FIC/N2032", name="Produce Toned, Fat, Low-Fat & Flavored Milk",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC3", name="Operate pasteurization equipment",
                           description="Run pasteurizer at correct temperature-time parameters"),
                Competency(code="PC4", name="Standardize milk",
                           description="Adjust fat and SNF content to required specifications"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="FIC/N2033", name="Carry Out Post-Production Activities",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC5", name="Package dairy products",
                           description="Fill, seal and label dairy products per standards"),
                Competency(code="PC6", name="Maintain production records",
                           description="Record batch data, quality test results, equipment logs"),
            ],
            provenance=_PROTO_PROV,
        ),
        QualificationNOS(
            code="FIC/N9906", name="Apply Food Safety Guidelines",
            core_or_elective="core", nsqf_level=4,
            competencies=[
                Competency(code="PC7", name="Follow FSSAI food safety standards",
                           description="Implement HACCP principles, maintain hygiene, handle allergens"),
            ],
            provenance=_PROTO_PROV,
        ),
    ],
)

# ══════════════════════════════════════════════════════════════════════
# Qualification Catalogue
# ══════════════════════════════════════════════════════════════════════
QUALIFICATION_CATALOGUE: dict[str, Qualification] = {
    q.id: q for q in [QUAL_TRACTOR, QUAL_ELECTRICAL, QUAL_DAIRY]
}

# ══════════════════════════════════════════════════════════════════════
# Demo Beneficiary
# ══════════════════════════════════════════════════════════════════════
DEMO_BENEFICIARY = Beneficiary(
    id="demo-beneficiary-001",
    name="Demo Beneficiary",
    age_group="25-30",
    education="10th Pass",
    district="Varanasi",
    preferred_language="Hindi",
    current_livelihood="Informal farm machinery repair",
    work_experience="5+ years working with father on tractor and pump repairs",
    employment_preference="employment",
    mobility_radius_km=50,
    data_origin=ProvenanceOrigin.SYNTHETIC,
    raw_statement=(
        "Main tractor aur pump repair karta hoon, papa ke saath kaam karta hoon. "
        "Chhoti-moti machine repair kar leta hoon, lekin certificate nahi hai."
    ),
    interests=["tractor repair", "mechanical work", "farm machinery"],
)

# ══════════════════════════════════════════════════════════════════════
# In-memory stores (populated at startup)
# ══════════════════════════════════════════════════════════════════════
beneficiaries: dict[str, Beneficiary] = {}
pathway_results: dict[str, CandidatePathway] = {}
decisions: dict[str, dict] = {}
