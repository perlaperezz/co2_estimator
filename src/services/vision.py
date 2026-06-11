import io
import json
import base64
from typing import List, Tuple, Optional
from PIL import Image

from google import genai
from src.models.invoice import InvoiceItem
from src.config import settings


EXTRACTION_PROMPT = """You are an invoice data extraction system. Analyze this invoice image and extract ALL line items as JSON.

Return ONLY valid JSON (no markdown, no explanation):
{
  "line_items": [
    {
      "description": "item description",
      "quantity": 1.0,
      "unit": "kg",
      "unit_price": 10.00,
      "total_price": 10.00
    }
  ],
  "invoice_total": 100.00,
  "invoice_number": "INV-001",
  "supplier": "Supplier Name",
  "date": "2024-01-15"
}

Rules:
- Extract EVERY line item. Do not skip any.
- quantity: default to 1 if not clearly specified
- unit: extract the unit of measure (hours, kg, tonnes, container, ticket, night, box, etc.)
- unit_price: set to null if not clearly shown on the invoice
- total_price: the line total shown on the invoice
- invoice_total: the grand total on the invoice
- Strip currency symbols ($, €, £) from prices — return only the number
- If a price contains commas (e.g. 1,200.00), keep the decimal but remove the comma
- If you cannot identify any line items, return empty line_items array with invoice_total: 0
"""


def _pdf_to_images(file_bytes: bytes, dpi: int = 200) -> List[bytes]:
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images: List[bytes] = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        images.append(img_bytes)
    doc.close()
    return images


def _call_gemini(image_bytes: bytes) -> dict:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    img_ref = genai.types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/png",
    )
    response = client.models.generate_content(
        model=settings.VISION_MODEL,
        contents=[EXTRACTION_PROMPT, img_ref],
        config={
            "response_mime_type": "application/json",
        },
    )
    text = (response.text or "").strip()
    if not text:
        return {"line_items": [], "invoice_total": 0}
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


def _parse_items(data: dict) -> Tuple[List[InvoiceItem], float]:
    items: List[InvoiceItem] = []
    for row in data.get("line_items", []):
        desc = (row.get("description") or "").strip()
        if not desc:
            continue
        qty = float(row["quantity"]) if row.get("quantity") is not None else 1.0
        unit = row.get("unit") or None
        unit_price = float(row["unit_price"]) if row.get("unit_price") is not None else None
        total_price = float(row["total_price"]) if row.get("total_price") is not None else None
        items.append(InvoiceItem(
            description=desc,
            quantity=qty,
            unit=unit,
            unit_price=unit_price,
            total_price=total_price,
        ))
    invoice_total = float(data.get("invoice_total") or 0)
    return items, invoice_total


def extract_from_pdf_vision(file_bytes: bytes) -> Optional[Tuple[List[InvoiceItem], float]]:
    if not settings.GEMINI_API_KEY:
        return None
    try:
        page_images = _pdf_to_images(file_bytes, dpi=200)
        all_items: List[InvoiceItem] = []
        total = 0.0
        for img_bytes in page_images:
            data = _call_gemini(img_bytes)
            items, page_total = _parse_items(data)
            all_items.extend(items)
            if page_total > 0:
                total = page_total
        if not all_items:
            return None
        return all_items, total
    except Exception:
        return None
