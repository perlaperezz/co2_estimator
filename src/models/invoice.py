from typing import Optional, Dict, List
from pydantic import BaseModel


class InvoiceItem(BaseModel):
    description: str
    quantity: float = 1
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    matched_item: Optional[str] = None
    matched_unit: Optional[str] = None
    co2_kg: Optional[float] = None
    co2_factor_used: Optional[float] = None
    estimate_method: str = "pending"


class AnalysisResult(BaseModel):
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    total_amount: float = 0
    currency: str = "USD"
    line_items: List[InvoiceItem] = []
    total_co2_kg: float = 0
    category_breakdown: Dict[str, float] = {}
