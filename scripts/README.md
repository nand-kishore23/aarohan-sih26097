# SCRIPTS

Planned scripts:

- `extract_qualification_source.py`
- `normalize_qualification.py`
- `validate_qualification_catalogue.py`
- `generate_synthetic_profiles.py`
- `calculate_district_signals.py`
- `export_evidence_brief.py`

No script should bypass:

```text
RAW → NORMALIZED → VALIDATED → CANONICAL
```

Do not write a script that directly turns arbitrary web text into production qualification records.
