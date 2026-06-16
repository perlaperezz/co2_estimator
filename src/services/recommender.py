from typing import List, Dict
from src.models.invoice import InvoiceItem
from src.models.floraspay import FlorasProject, ProjectAllocation, FlorasCalculation, Recommendation
from src.services import projects as project_service
from src.services import florascalc
from src.services.categorizer import get_project_category_mapping
from src.config import settings


def get_recommendation(
    total_co2_kg: float,
    line_items: List[InvoiceItem],
    transaction_value: float,
    rate: float = settings.FLORAS_BASE_RATE,
) -> Recommendation:
    all_projects = project_service.load_projects()
    category_mapping = get_project_category_mapping()

    invoice_categories = set()
    for item in line_items:
        if item.category:
            invoice_categories.add(item.category)

    matched_project_cats: set = set()
    for cat in invoice_categories:
        for proj_cat in category_mapping.get(cat, []):
            matched_project_cats.add(proj_cat)

    if not matched_project_cats:
        matched_project_cats = set(category_mapping.get("General", []))

    project_category_weights: Dict[str, float] = {}
    for inv_cat in invoice_categories:
        for proj_cat in category_mapping.get(inv_cat, []):
            project_category_weights[proj_cat] = (
                project_category_weights.get(proj_cat, 0) + 1.0
            )

    total_weight = sum(project_category_weights.values()) or 1.0
    for k in project_category_weights:
        project_category_weights[k] /= total_weight

    candidate_projects = [
        p for p in all_projects if p.category in matched_project_cats
    ]

    if not candidate_projects:
        candidate_projects = all_projects

    total_floras = florascalc.calc_floras(transaction_value, rate)

    category_floras: Dict[str, float] = {}
    for p in candidate_projects:
        weight = project_category_weights.get(p.category, 0.0)
        if not category_floras:
            category_floras[p.category] = total_floras / len(set(p.category for p in candidate_projects))

    floras_per_category = total_floras / len(set(p.category for p in candidate_projects)) if candidate_projects else total_floras

    allocations: List[ProjectAllocation] = []
    total_offset_kg = 0.0
    total_allocated_floras = 0.0

    assigned_categories = set()
    for p in candidate_projects:
        if p.category not in assigned_categories:
            assigned_categories.add(p.category)
            alloc_floras = floras_per_category
            offset = florascalc.calc_offset(p, alloc_floras)
            allocations.append(ProjectAllocation(
                project=p,
                floras_allocated=round(alloc_floras, 2),
                co2_offset_kg=round(offset, 2),
            ))
            total_offset_kg += offset
            total_allocated_floras += alloc_floras

    avg_co2e = total_offset_kg / total_allocated_floras if total_allocated_floras > 0 else 0.0
    floras_calc = florascalc.calc_floras_calculation(
        transaction_value, total_co2_kg, total_allocated_floras, avg_co2e
    )

    recommended_rate = rate
    if floras_calc.gap_kg > 0 and avg_co2e > 0:
        floras_needed = floras_calc.gap_kg / avg_co2e
        contribution_needed = floras_needed * settings.FLORAS_TO_USD
        recommended_rate = (contribution_needed / transaction_value * 100) if transaction_value > 0 else rate

    recommended_rate = max(rate, round(recommended_rate, 2))

    if floras_calc.fully_offset:
        summary = f"Your current {rate}% Floras allocation fully covers this invoice's CO₂ footprint."
    else:
        coverage = floras_calc.offset_percentage
        summary = (
            f"Your current {rate}% rate offsets {coverage}% ({floras_calc.current_offset_kg:.0f} kg CO₂) "
            f"of {total_co2_kg:.0f} kg CO₂ total. "
            f"Increase to {recommended_rate}% to fully offset the remaining {floras_calc.gap_kg:.0f} kg CO₂."
        )

    return Recommendation(
        current_rate=rate,
        recommended_rate=recommended_rate,
        rate_increase=round(recommended_rate - rate, 2),
        floras_calculation=floras_calc,
        allocations=allocations,
        summary=summary,
        total_co2_kg=total_co2_kg,
    )
