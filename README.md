# CO₂ Estimator

Climate intelligence for your supply chain — estimate the carbon footprint of any invoice and fund the right offset projects through Floras.

## Overview

CO₂ Estimator reads uploaded invoices (text paste or PDF), extracts line items via AI-powered vision, estimates each item's CO₂ footprint using a curated knowledge base of emission factors, calculates how much a supplier's Floras contribution offsets, and recommends optimal contribution rates and climate projects.

Built for [**Floras**](https://floras.io), the climate currency platform that turns business transactions into climate action.

## Key Features

- **PDF + text invoice parsing** — Vision-first extraction via Gemini API with automatic fallback to regex-based text parsing
- **Line-item categorization** — Classifies items into Freight, Travel, Energy, Materials, Packaging, Services, Waste, and Water
- **CO₂ estimation** — Matches line items against a distilled knowledge base of EPA, DEFRA, OWID, and EDGAR emission factors
- **Floras offset calculation** — Computes offset at the 1.25% base rate (or any custom rate)
- **Gap analysis** — Identifies unaddressed CO₂ and recommends rate increases
- **Interactive allocation dashboard** — Drag sliders to distribute Floras across matched projects with live CO₂ offset and gap tracking
- **Project matching** — Recommends the best Floras projects for each invoice's emission profile
- **Maximize Impact** — One-click redistribution to prioritize highest CO₂e/Flora projects

## Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | Python 3.9+, FastAPI |
| Frontend | Jinja2 templates + Tailwind CSS (CDN) |
| Invoice parsing | Gemini Flash vision API + pymupdf + pypdf/regex fallback |
| Emission factors | Local CSV distilled from EPA, DEFRA, OWID, EDGAR |
| Climate projects | Local CSV with 18 Floras projects and CO₂e-per-Flora rates |

## Data Sources

The knowledge base (`data/knowledge_base.csv`) compiles emission factors from:

| Source | Description |
|--------|-------------|
| **DEFRA** (UK, 2024) | Freight, travel, energy, materials, packaging, waste, water |
| **EPA** (US) | Grid electricity, natural gas, GDP-based estimates |
| **OWID** | GDP-based CO₂ per dollar (Global, US, EU, China) |
| **IEA / EDGAR** | Global average grid electricity |

The project catalog (`data/floras_projects.csv`) contains 18 real carbon-reduction projects across 11 categories with provider-sourced images.

## How It Works

```
Upload invoice → AI extracts line items → Categorize each item →
Match emission factors → Calculate CO₂ footprint →
Compute Floras offset → Analyze gap →
Recommend rate + projects → Interactive allocation dashboard
```

## Local Setup

```bash
# Clone the repository
git clone https://github.com/perlaperezz/co2_estimator.git
cd co2_estimator

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key (required for PDF vision parsing)
export GEMINI_API_KEY="your-key-here"

# Run the server
python3 -m uvicorn src.main:app --reload --port 8000
```

Open **http://localhost:8000** in your browser. Paste an invoice or upload a PDF to get started. A sample invoice is pre-loaded for quick testing.

## Floras & This Tool

[**Floras**](https://floras.io) is a climate currency platform where suppliers contribute a small percentage of each transaction (base rate: 1.25%) to fund verified carbon-reduction projects. $1 = 1 Flora, and enterprises direct their Floras toward the projects they choose.

CO₂ Estimator is the intelligence layer of the Floras ecosystem. It gives enterprises visibility into their supply chain emissions and shows exactly how far their Floras contribution goes — turning every transaction into measurable climate action.

## Screenshot

<p align="center">
 <img
    src="https://github.com/user-attachments/assets/0509b7c3-3ddb-4f3a-a8a4-ef9b5a35fc82"
    alt="Invoice upload screen"
    width="49%"
  />
  <img
    src="https://github.com/user-attachments/assets/2608561a-fd70-4a53-a7c9-98de53d8d10f"
    alt="Invoice analysis results"
    width="49%"
  />
</p>

## Acknowledgements

- Emission factor data from the UK Department for Environment, Food & Rural Affairs (DEFRA), the US Environmental Protection Agency (EPA), Our World in Data (OWID), and the Emissions Database for Global Atmospheric Research (EDGAR)
- Climate project images and data provided by Patch, CNaught, and FLORAS
- Built with FastAPI, Jinja2, Tailwind CSS, and Google Gemini
