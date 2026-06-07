from typing import Optional
from src.models.invoice import InvoiceItem
from src.services import kb
from src.services import categorizer


def estimate_item(item: InvoiceItem) -> InvoiceItem:
    if item.category is None:
        cat, subcat = categorizer.categorize_item(item.description)
        item.category = cat
        item.subcategory = subcat

    match = kb.find_match(item.description, category_hint=item.category)

    co2_kg = None
    method = "rough"

    if match is not None:
        factor = float(match["co2_kg"])
        unit = str(match["unit"])
        item.matched_item = str(match["item"])
        item.matched_unit = unit
        item.co2_factor_used = factor

        if unit in ("USD",) and item.total_price is not None:
            co2_kg = factor * item.total_price
            method = "spend"
        elif unit in ("kWh", "litre", "m3", "tonne", "kg", "km", "miles",
                      "tonne.km", "passenger.km", "room.night", "mmBtu"):
            co2_kg = factor * item.quantity
            method = "exact"
        elif item.total_price is not None:
            co2_kg = factor * item.quantity
            method = "exact"
        else:
            co2_kg = factor * item.quantity
            method = "exact"
    else:
        cat_avg = kb.get_category_average(item.category if item.category else "")
        if cat_avg is not None:
            co2_kg = cat_avg * item.quantity
            item.co2_factor_used = cat_avg
            method = "category_avg"
        elif item.total_price is not None:
            gdp_factor = kb.get_gdp_fallback()
            co2_kg = gdp_factor * item.total_price
            item.co2_factor_used = gdp_factor
            method = "spend"
        else:
            co2_kg = item.quantity * 0.1
            item.co2_factor_used = 0.1
            method = "floor"

    item.co2_kg = round(co2_kg, 4) if co2_kg is not None else None
    item.estimate_method = method
    return item
