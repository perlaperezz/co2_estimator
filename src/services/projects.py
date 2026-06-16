import csv
from typing import List, Optional
from src.models.floraspay import FlorasProject
from src.config import settings

_projects_cache: Optional[List[FlorasProject]] = None


def load_projects() -> List[FlorasProject]:
    global _projects_cache
    if _projects_cache is not None:
        return _projects_cache

    projects: List[FlorasProject] = []
    with open(settings.PROJECTS_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_url = row.get("image_url", "").strip('"')
            if raw_url.lower() == "floras.png":
                raw_url = "/static/floras_logo.jpeg"
            projects.append(FlorasProject(
                id=int(row["id"]),
                name=row["name"],
                category=row["category"],
                co2e_per_flora=float(row["co2e_per_flora"]),
                location=row["location"],
                description=row["description"],
                provider=row["provider"],
                image_url=raw_url,
            ))
    _projects_cache = projects
    return projects
