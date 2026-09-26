"""Deterministic Skill Extraction Engine for Prototype."""

from .models import SkillObservation, Provenance, ProvenanceOrigin


# Simple keyword mapping for the prototype demo
# (A real implementation would use an LLM for extraction + vector DB for normalization)
KEYWORD_MAPPING = {
    "tractor": ("tractor_repair", "Tractor repair experience mentioned"),
    "pump": ("pump_repair", "Pump repair experience mentioned"),
    "machine": ("machine_repair", "General machinery repair experience mentioned"),
    "electrical": ("electrical_repair", "Electrical repair experience mentioned"),
    "wire": ("wiring", "Wiring/cable experience mentioned"),
    "dairy": ("dairy_processing", "Dairy handling experience mentioned"),
    "milk": ("milk_testing", "Milk handling experience mentioned"),
    "repair": ("mechanical_troubleshooting", "General repair troubleshooting mentioned"),
    "phone": ("mobile_phone_repair", "Mobile phone repair experience mentioned"),
    "mobile": ("mobile_phone_repair", "Mobile phone repair experience mentioned"),
    "display": ("display_replacement", "Display work experience mentioned"),
    "charging": ("charging_fault_repair", "Charging-fault work experience mentioned"),
    "solder": ("soldering", "Soldering experience mentioned"),
}


def extract_skills(raw_text: str) -> list[SkillObservation]:
    """
    Extracts normalized skills from raw text using deterministic keyword matching.
    """
    observations = []
    text_lower = raw_text.lower()
    
    # We use a set to avoid duplicates if multiple keywords map to the same skill
    # (though in this simple mapping they are 1:1)
    seen_skills = set()
    
    for keyword, (normalized_skill, evidence) in KEYWORD_MAPPING.items():
        if keyword in text_lower and normalized_skill not in seen_skills:
            seen_skills.add(normalized_skill)
            
            # Extract a snippet of text around the keyword for evidence
            # (In this prototype, we just use the predefined evidence string or the whole sentence)
            
            obs = SkillObservation(
                raw_skill=keyword,
                normalized_skill=normalized_skill,
                evidence_text=f"Extracted from: '...{keyword}...' - {evidence}",
                source_type=ProvenanceOrigin.SELF_REPORTED,
                provenance=Provenance(origin=ProvenanceOrigin.SELF_REPORTED)
            )
            observations.append(obs)
            
    return observations
