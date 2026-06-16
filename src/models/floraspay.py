from pydantic import BaseModel


class FlorasProject(BaseModel):
    id: int
    name: str
    category: str
    co2e_per_flora: float
    location: str
    description: str
    provider: str
    image_url: str = ""


class ProjectAllocation(BaseModel):
    project: FlorasProject
    floras_allocated: float
    co2_offset_kg: float


class FlorasCalculation(BaseModel):
    total_contribution: float
    total_floras: float
    current_offset_kg: float
    gap_kg: float
    fully_offset: bool
    offset_percentage: float


class Recommendation(BaseModel):
    current_rate: float
    recommended_rate: float
    rate_increase: float
    floras_calculation: FlorasCalculation
    allocations: list[ProjectAllocation] = []
    summary: str
    total_co2_kg: float = 0
