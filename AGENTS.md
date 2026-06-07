# CO2 Estimator — Agent Context

## Project Overview

**CO2 Estimator** is the intelligence layer for **Floras** (floras.io), a platform that turns business transactions into climate action. Suppliers contribute a small percentage of each transaction (base rate: 1.25%) which is converted into "Floras" (climate currency) that enterprises direct toward verified carbon reduction projects.

This tool reads uploaded invoices, estimates their CO2 footprint, calculates how much the 1.25% Floras allocation offsets, and recommends optimal contribution rates and project types.

## Floras Context

- **Floras** is both the company and the climate currency unit
- **1.25% base rate** — supplier contributes this percentage of each transaction
- **Floras currency** — converted from the contribution ($1 = 1 Flora), used to fund carbon projects
- **Projects** — 18 projects across 11 categories (reforestation, SAF, biochar, renewable energy, etc.)
- **Users** — enterprises who receive invoices from suppliers and want to understand/improve their climate impact

## Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | Python 3.9+, FastAPI |
| Frontend | Jinja2 templates + Tailwind CSS (CDN) |
| Invoice parsing | Regex-based line item extraction (primary) + pypdf (text PDFs) + pdf2image/tesseract (scanned PDFs, optional) |
| AI orchestration | OpenCode with `deepseek-v4-flash` for orchestrator (future: invoice reading + analysis) |
| CO2 knowledge base | Local CSV (`data/knowledge_base.csv`) distilled from EPA, DEFRA, OWID, EDGAR |
| Floras projects | Local CSV (`data/floras_projects.csv`) with 18 projects and co2e_per_flora rates |
| Demo stability | Always prioritized over new features |

## Agent Role Mapping (oh-my-opencode-slim.json)

| Agent | Model | Role |
|-------|-------|------|
| **orchestrator** | `deepseek-v4-flash` | Invoice reading, line-item extraction, CO2 estimation, gap analysis, recommendation generation |
| **fixer** | `deepseek-v4-flash` | Backend implementation, data processing |
| **librarian** | `minimax-m2.7` | Web search, context retrieval for emission factors |
| **oracle** | `deepseek-v4-pro` | Strategic advice, architecture review |
| **designer** | `kimi-k2.6` | UI/UX, frontend polish |
| **observer** | `kimi-k2.6` | Monitoring, logging, demo walkthrough |

## Invoice Processing Pipeline (Primary: PDF)

1. User uploads PDF invoice via web UI
2. pdf2image converts PDF pages to images
3. OCR (pytesseract) extracts raw text
4. DeepSeek V4 Flash (orchestrator) parses line items from text
5. Each line item is categorized (freight, materials, energy, travel, services, packaging)
6. knowledge_base.csv is queried for matching CO2 factors
7. CO2 footprint is calculated per item and totaled
8. Floras offset = total_transaction_value × 1.25% × offset_rate_from_knowledge_base
9. Gap = total_CO2 - Floras_offset
10. Recommendation engine determines if 1.25% is sufficient or suggests higher rate
11. Project matching suggests best Floras projects for the emission profile

## Coding Rules

- **Demo stability beats new features** — if a feature risks breaking the demo flow, cut it
- All Python code must have type hints
- No dead code, commented-out code, or unused imports
- FastAPI route handlers should be thin — logic goes in `services/`
- Pydantic models for all request/response schemas
- knowledge_base.csv is the single source of truth for emission factors
- No hardcoded magic numbers — pull from config or KB
- Frontend must be responsive and presentable (mentor demo)
- The demo must tell a clear story in under 10 minutes

## Folder Structure

```
co2_estimator/
├── AGENTS.md
├── TODO.md
├── LOG.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/               # downloaded source files (gitignored)
│   ├── processed/          # cleaned extracted CSVs
│   └── knowledge_base.csv  # unified emission factor lookup table
├── src/
│   ├── __init__.py
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── invoice.py      # InvoiceItem, Invoice, AnalysisResult
│   │   └── floraspay.py    # FlorasCalculation, Recommendation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py       # PDF → image → OCR → text
│   │   ├── categorizer.py  # classify line items
│   │   ├── estimator.py    # CO2 estimation from KB
│   │   ├── florascalc.py   # Floras offset math
│   │   ├── recommender.py  # rate + project recommendations
│   │   └── kb.py           # knowledge_base.csv loader/query
│   ├── data/
│   │   ├── __init__.py
│   │   └── seed.py         # seed knowledge_base from raw sources
│   └── web/
│       ├── __init__.py
│       ├── routes.py        # FastAPI routes
│       ├── templates/
│       │   ├── base.html
│       │   └── index.html
│       └── static/
│           └── style.css
└── tests/
    ├── __init__.py
    └── test_estimator.py
```

## Key Demo Flow (under 10 minutes)

1. Land on upload page → upload a sample invoice PDF (~30s)
2. See parsed line items with categories and CO2 estimates (~2 min)
3. See total CO2 footprint (~30s)
4. See Floras offset at 1.25% (~30s)
5. See the gap (unaddressed CO2) (~15s)
6. See recommendation: keep or increase rate + how much (~1 min)
7. See matched Floras projects (~1 min)
8. Q&A (~4 min)
