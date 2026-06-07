# CO2 Estimator — TODO

## MVP Demo

- [x] Project initialization (AGENTS.md, TODO.md, LOG.md, .gitignore, data dirs)
- [x] Download source data (EPA, DEFRA, OWID, EDGAR)
- [x] Create knowledge_base.csv with distilled emission factors
- [x] Create `requirements.txt` (fastapi, uvicorn, pdf2image, pytesseract, pandas, jinja2, python-multipart, pypdf)
- [x] Implement `src/data/seed.py` — script to rebuild knowledge_base.csv from raw sources
- [x] Implement `src/services/kb.py` — knowledge base loader and query engine
- [x] Implement `src/services/parser.py` — text + PDF parse with regex line-item extraction
- [x] Implement `src/services/categorizer.py` — classify invoice line items
- [x] Implement `src/services/estimator.py` — CO2 estimation per item
- [x] Implement `src/services/projects.py` — floras_projects.csv loader
- [x] Implement `src/services/florascalc.py` — Floras offset calculation
- [x] Implement `src/services/recommender.py` — rate + project recommendations
- [x] Implement `src/models/invoice.py` — Pydantic schemas
- [x] Implement `src/models/floraspay.py` — Pydantic schemas
- [x] Implement `src/config.py` — settings
- [x] Implement `src/web/routes.py` — FastAPI endpoints
- [x] Build `src/web/templates/base.html` — layout shell
- [x] Build `src/web/templates/index.html` — upload + results page
- [x] Wire up `src/main.py` — FastAPI app entry point
- [x] Test end-to-end demo flow with sample invoice (paste text)
- [ ] Test PDF upload flow
- [ ] Polish UI for mentor demo
- [ ] Write demo script (~10 min walkthrough)

## Nice to Have

- [ ] Multi-currency invoice support
- [ ] Multi-language invoice OCR
- [ ] Batch invoice upload (CSV or ZIP)
- [ ] PDF report export
- [ ] Historical analysis dashboard (charts over time)
- [ ] User authentication
- [ ] Floras project detail pages with impact metrics
- [ ] Supplier-facing view (show suppliers their contribution impact)
- [ ] API for programmatic access
- [ ] Real-time emission factor updates via webhook
- [ ] Integration with Floras platform API
- [ ] Mobile-responsive design
- [ ] Dark mode
- [ ] i18n / l10n
