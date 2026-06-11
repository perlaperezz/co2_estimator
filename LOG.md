# Changelog

## 2026-06-05
- Project initialized — foundational files, folder structure, data downloads, knowledge_base.csv
- Built complete app: FastAPI backend, Jinja2/Tailwind frontend, 7 services, Pydantic models
- Invoice pipeline: text paste + PDF upload (pypdf) → regex parsing → categorization → KB estimation → Floras offset → project matching → rate recommendation
- 11 project categories mapped to invoice line items, 18 Floras projects with co2e_per_flora rates
- Confirmed end-to-end with sample invoice: 24,063 kg CO₂ footprint, fully offset at 1.25%, project recommendations generated

## 2026-06-07
- Debugged template rendering: fixed result context dict key mismatches, recommendation object type-checking, and variable scoping
- Fixed config.py BASE_DIR resolution (2 .parent calls instead of 3)
- Verified full pipeline end-to-end: startup → GET / → POST /analyze → results render correctly
- Tested with sample invoice ($51,900): 24,063 kg CO₂ footprint, 121,893 kg offset at 1.25%, gap fully covered, recommendation to keep 1.25%
- Committed 29 files (1,105 lines) and pushed to GitHub

## 2026-06-11
- Relaxed parser regex patterns (\s{2,} → \s+) to handle single-space column separators from pypdf extraction
- Added multi-line grouping fallback (description line + price line pairing) for common pypdf output format
- Added header/label keyword filtering to prevent column headers and label-value lines from being parsed as items
- Added raw text preview in error response when parsing yields 0 items
- Confirmed parser still fails on arbitrary real-world PDF layouts — regex approach fundamentally limited
- Decision: switch to vision-based approach (GPT-4o or similar) for reliable line-item extraction
- Created sample invoice with 7 line items ($51,900 total) for demo testing
