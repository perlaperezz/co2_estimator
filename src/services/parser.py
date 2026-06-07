import re
import io
from typing import List, Tuple, Optional
from src.models.invoice import InvoiceItem


def parse_text(text: str) -> Tuple[List[InvoiceItem], float]:
    lines = text.strip().split("\n")
    items: List[InvoiceItem] = []
    total_amount: float = 0.0
    captured_total: Optional[float] = None
    metadata_lines = ["invoice", "date", "total", "subtotal", "tax", "page", "supplier",
                      "from:", "bill to", "ship to", "payment", "due", "reference", "note"]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        lower = stripped.lower()
        if any(m in lower for m in ["total:", "total "]):
            m = re.search(r'[\$€£]?\s*([\d,]+\.?\d*)', stripped)
            if m:
                captured_total = _parse_amount(m.group(1))
            continue
        if any(stripped.lower().startswith(m) for m in metadata_lines):
            continue
        if re.match(r'^[\d\s\.\-,]*$', stripped):
            continue
        if len(stripped) < 4:
            continue

        item = _parse_line(stripped)
        if item is not None:
            items.append(item)
            if item.total_price is not None:
                total_amount += item.total_price

    final_total = captured_total if captured_total is not None else total_amount

    if items and captured_total and abs(total_amount - captured_total) > 1:
        scale = captured_total / total_amount if total_amount > 0 else 1.0
        for item in items:
            if item.total_price is not None:
                item.total_price = round(item.total_price * scale, 2)
        total_amount = captured_total

    return items, round(final_total, 2)


def _parse_amount(s: str) -> float:
    cleaned = s.strip().replace(",", "").replace("$", "").replace("€", "").replace("£", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_line(line: str) -> Optional[InvoiceItem]:
    patterns = [
        # 5-column table: Description  Qty  Unit  UnitPrice  Total
        (r'^(.+?)\s{2,}(\d+(?:\.\d+)?)\s{2,}([a-zA-Z/]+)\s{2,}\$?([\d,]+\.?\d*)\s{2,}\$?([\d,]+\.?\d*)\s*$',
         lambda m: InvoiceItem(
             description=m.group(1).strip(),
             quantity=float(m.group(2)),
             unit=m.group(3).strip(),
             unit_price=_parse_amount(m.group(4)),
             total_price=_parse_amount(m.group(5)),
         )),
        # Qty x Description @ Price = Total
        (r'(\d+(?:\.\d+)?)\s*x?\s*(.+?)\s+@\s*\$?([\d,]+\.?\d*)\s*=\s*\$?([\d,]+\.?\d*)',
         lambda m: InvoiceItem(
             description=m.group(2).strip(),
             quantity=float(m.group(1)),
             unit_price=_parse_amount(m.group(3)),
             total_price=_parse_amount(m.group(4)),
         )),
        # Qty Description @ Price
        (r'(\d+(?:\.\d+)?)\s+(.+?)\s+@\s*\$?([\d,]+\.?\d*)',
         lambda m: InvoiceItem(
             description=m.group(2).strip(),
             quantity=float(m.group(1)),
             unit_price=_parse_amount(m.group(3)),
             total_price=float(m.group(1)) * _parse_amount(m.group(3)),
         )),
        # Description ...... Total
        (r'^(.+?)\s+\.{2,}\s*\$?([\d,]+\.?\d*)\s*$',
         lambda m: InvoiceItem(
             description=m.group(1).strip(),
             quantity=1,
             total_price=_parse_amount(m.group(2)),
         )),
        # Qty followed by Description and Price (no unit column)
        (r'^(\d+(?:\.\d+)?)\s+(.+?)\s{2,}\$?([\d,]+\.?\d*)\s*$',
         lambda m: InvoiceItem(
             description=m.group(2).strip(),
             quantity=float(m.group(1)),
             total_price=_parse_amount(m.group(3)),
         )),
        # Description ... Price (simple line)
        (r'^(.+?)\s{2,}\$?([\d,]+\.?\d*)\s*$',
         lambda m: InvoiceItem(
             description=m.group(1).strip(),
             quantity=1,
             total_price=_parse_amount(m.group(2)),
         )),
    ]

    for pattern, builder in patterns:
        m = re.match(pattern, line.strip())
        if m:
            item = builder(m)
            if item.description and len(item.description) > 1:
                return item
    return None


def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    try:
        from pdf2image import convert_from_bytes
        import pytesseract
        images = convert_from_bytes(file_bytes)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    return None
