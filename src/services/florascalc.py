from src.models.floraspay import FlorasProject, FlorasCalculation
from src.config import settings


def calc_floras(transaction_value: float, rate: float = settings.FLORAS_BASE_RATE) -> float:
    contribution = transaction_value * (rate / 100.0)
    return contribution / settings.FLORAS_TO_USD


def calc_offset(project: FlorasProject, floras: float) -> float:
    return floras * project.co2e_per_flora


def calc_floras_calculation(
    transaction_value: float,
    total_co2_kg: float,
    floras_allocated: float,
    avg_co2e_per_flora: float,
) -> FlorasCalculation:
    total_contribution = transaction_value * (settings.FLORAS_BASE_RATE / 100.0)
    current_offset_kg = floras_allocated * avg_co2e_per_flora
    gap_kg = max(0.0, total_co2_kg - current_offset_kg)
    offset_percentage = (current_offset_kg / total_co2_kg * 100) if total_co2_kg > 0 else 0.0
    fully_offset = gap_kg <= 0.0

    return FlorasCalculation(
        total_contribution=round(total_contribution, 2),
        total_floras=round(floras_allocated, 2),
        current_offset_kg=round(current_offset_kg, 2),
        gap_kg=round(gap_kg, 2),
        fully_offset=fully_offset,
        offset_percentage=round(offset_percentage, 1),
    )
