from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

from src.services.parser import parse_text, extract_from_pdf
from src.services.estimator import estimate_item
from src.services.recommender import get_recommendation
from src.config import settings

router = APIRouter()
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sample_path = settings.DATA_DIR / "sample_invoice.txt"
    sample_text = ""
    if sample_path.exists():
        sample_text = sample_path.read_text()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "sample_text": sample_text},
    )


@router.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    invoice_text: Optional[str] = Form(None),
    pdf_file: Optional[UploadFile] = File(None),
    total_amount: float = Form(0.0),
    rate: float = Form(settings.FLORAS_BASE_RATE),
):
    items: list = []
    parsed_total: float = 0.0
    raw_text: str = ""

    if pdf_file and pdf_file.filename and pdf_file.filename.lower().endswith(".pdf"):
        file_bytes = await pdf_file.read()
        result = extract_from_pdf(file_bytes)
        if result == "QUOTA":
            return templates.TemplateResponse("index.html", {
                "request": request,
                "result": None,
                "error": "Gemini API free quota reached for today. Paste invoice text directly or try again tomorrow.",
                "sample_text": "",
            })
        if result is None:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "result": None,
                "error": "Could not extract line items from PDF. Try pasting invoice text instead.",
                "sample_text": "",
            })
        items, parsed_total = result
    elif invoice_text:
        raw_text = invoice_text
        items, parsed_total = parse_text(raw_text)
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": None,
            "error": "Please provide invoice text or upload a PDF.",
            "sample_text": "",
        })

    if not items:
        preview = raw_text[:500] if raw_text else ""
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": None,
            "error": "Could not parse any line items. Raw text received:<br><pre style='font-size:12px;max-height:200px;overflow:auto'>" + preview + "</pre>",
            "sample_text": raw_text,
        })

    effective_total = total_amount if total_amount > 0 else parsed_total

    for item in items:
        estimate_item(item)

    total_co2 = sum(item.co2_kg for item in items if item.co2_kg is not None)

    category_breakdown = {}
    for item in items:
        cat = item.category or "Uncategorized"
        co2 = item.co2_kg or 0
        category_breakdown[cat] = category_breakdown.get(cat, 0) + co2

    recommendation = get_recommendation(total_co2, items, effective_total, rate)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": {
            "line_items": items,
            "total_co2_kg": round(total_co2, 2),
            "category_breakdown": dict(sorted(category_breakdown.items(), key=lambda x: -x[1])),
            "total_amount": effective_total,
            "currency": "USD",
            "recommendation": recommendation,
        },
        "error": None,
        "sample_text": "",
    })
