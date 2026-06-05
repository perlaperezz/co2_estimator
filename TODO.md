# CO2 Estimator — TODO

## MVP Demo

- [x] Project initialization (AGENTS.md, TODO.md, LOG.md, .gitignore, data dirs)
- [x] Download source data (EPA, DEFRA, OWID, EDGAR)
- [x] Create knowledge_base.csv with distilled emission factors
- [ ] Create `requirements.txt` (fastapi, uvicorn, pdf2image, pytesseract, pandas, jinja2, python-multipart)
- [ ] Implement `src/data/seed.py` — script to rebuild knowledge_base.csv from raw sources
- [ ] Implement `src/services/kb.py` — knowledge base loader and query engine
- [ ] Implement `src/services/parser.py` — PDF upload → OCR → raw text
- [ ] Implement `src/services/categorizer.py` — classify invoice line items
- [ ] Implement `src/services/estimator.py` — CO2 estimation per item
- [ ] Implement `src/services/florascalc.py` — Floras offset calculation
- [ ] Implement `src/services/recommender.py` — rate + project recommendations
- [ ] Implement `src/models/invoice.py` — Pydantic schemas
- [ ] Implement `src/models/floraspay.py` — Pydantic schemas
- [ ] Implement `src/config.py` — settings
- [ ] Implement `src/web/routes.py` — FastAPI endpoints
- [ ] Build `src/web/templates/base.html` — layout shell
- [ ] Build `src/web/templates/index.html` — upload + results page
- [ ] Wire up `src/main.py` — FastAPI app entry point
- [ ] Test end-to-end demo flow with a sample PDF invoice
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
