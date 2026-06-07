# Changelog

## 2026-06-05
- Project initialized — foundational files, folder structure, data downloads, knowledge_base.csv
- Built complete app: FastAPI backend, Jinja2/Tailwind frontend, 7 services, Pydantic models
- Invoice pipeline: text paste + PDF upload (pypdf) → regex parsing → categorization → KB estimation → Floras offset → project matching → rate recommendation
- 11 project categories mapped to invoice line items, 18 Floras projects with co2e_per_flora rates
- Confirmed end-to-end with sample invoice: 24,063 kg CO₂ footprint, fully offset at 1.25%, project recommendations generated
