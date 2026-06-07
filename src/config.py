from pathlib import Path


class Settings:
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    KB_PATH: Path = DATA_DIR / "knowledge_base.csv"
    PROJECTS_PATH: Path = DATA_DIR / "floras_projects.csv"
    FLORAS_BASE_RATE: float = 1.25
    FLORAS_TO_USD: float = 1.0
    DEFAULT_CURRENCY: str = "USD"
    GDP_FALLBACK: float = 0.26


settings = Settings()
