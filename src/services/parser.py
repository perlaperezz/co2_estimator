import re
import io
from typing import List, Tuple, Optional
from src.models.invoice import InvoiceItem
from src.services.vision import extract_from_pdf_vision


def parse_text(text: str) -> Tuple[List[InvoiceItem], float]:
    lines = text.strip().split("\n")
    items: List[InvoiceItem] = []
    total_amount: float = 0.0
    captured_total: Optional[float] = None
    metadata_lines = ["invoice", "date", "total", "subtotal", "tax", "page", "supplier",
                      "from:", "bill to", "ship to", "payment", "due", "reference", "note",
                      "item", "qty", "description", "description:", "quantity:", "quantity",
                      "unit price:", "rate:", "amount:", "subtotal:", "total:"]

    pending_desc: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            pending_desc = None
            continue

        lower = stripped.lower()
        if any(m in lower for m in ["total:", "total "]):
            m = re.search(r'[\$€£]?\s*([\d,]+\.?\d*)', stripped)
            if m:
                captured_total = _parse_amount(m.group(1))
            pending_desc = None
            continue
        if any(lower.startswith(m) for m in metadata_lines):
            pending_desc = None
            continue

        # Pure-number line — could be a price for a pending description
        if re.match(r'^[\d\.]+$', stripped) and pending_desc is not None:
            price = _parse_amount(stripped)
            if price > 0:
                items.append(InvoiceItem(
                    description=pending_desc,
                    quantity=1,
                    total_price=price,
                ))
                total_amount += price
                pending_desc = None
                continue

        if re.match(r'^[\d\s\.\-,]*$', stripped):
            pending_desc = None
            continue
        if len(stripped) < 4:
            pending_desc = None
            continue

        item = _parse_line(stripped)
        if item is not None:
            items.append(item)
            if item.total_price is not None:
                total_amount += item.total_price
            pending_desc = None
            continue

        # Check if line is a standalone price — pair with previously pending description
        price_match = re.match(r'^\$?([\d,]+\.?\d*)\s*$', stripped)
        if price_match and pending_desc is not None:
            price = _parse_amount(price_match.group(1))
            items.append(InvoiceItem(
                description=pending_desc,
                quantity=1,
                total_price=price,
            ))
            total_amount += price
            pending_desc = None
            continue

        # Check if line ends with a price — try simple description + price parse
        end_price = re.search(r'^(.+?)\s+\$?([\d,]+\.?\d*)\s*$', stripped)
        if end_price:
            items.append(InvoiceItem(
                description=end_price.group(1).strip(),
                quantity=1,
                total_price=_parse_amount(end_price.group(2)),
            ))
            total_amount += _parse_amount(end_price.group(2))
            pending_desc = None
            continue

        # Save as pending description for next-line price pairing
        pending_desc = stripped

    final_total = captured_total if captured_total is not None else total_amount

    if items and captured_total and abs(total_amount - captured_total) > 1:
        scale = captured_total / total_amount if total_amount > 0 else 1.0
        for item in items:
            if item.total_price is not None:
                item.total_price = round(item.total_price * scale, 2)
        total_amount = captured_total

    return items, round(final_total, 2)


def extract_from_pdf(file_bytes: bytes) -> Optional[Tuple[List[InvoiceItem], float]]:
    result = extract_from_pdf_vision(file_bytes)
    if result is not None:
        return result
    return _extract_text_from_pdf_fallback(file_bytes)


def _extract_text_from_pdf_fallback(file_bytes: bytes) -> Optional[Tuple[List[InvoiceItem], float]]:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            items, total = parse_text(text)
            if items:
                return items, total
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
            items, total = parse_text(text)
            if items:
                return items, total
    except Exception:
        pass

    return None


def _parse_amount(s: str) -> float:
    cleaned = s.strip().replace(",", "").replace("$", "").replace("€", "").replace("£", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_line(line: str) -> Optional[InvoiceItem]:
    patterns = [
        # 5-column table: Description  Qty  Unit  UnitPrice  Total
        (r'^(.+?)\s+(\d+(?:\.\d+)?)\s+([a-zA-Z/]+)\s+\$?([\d,]+\.?\d*)\s+\$?([\d,]+\.?\d*)\s*$',
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
        (r'^(\d+(?:\.\d+)?)\s+(.+?)\s+\$?([\d,]+\.?\d*)\s*$',
         lambda m: InvoiceItem(
             description=m.group(2).strip(),
             quantity=float(m.group(1)),
             total_price=_parse_amount(m.group(3)),
         )),
        # Description ... Price (simple line)
        (r'^(.+?)\s+\$?([\d,]+\.?\d*)\s*$',
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
