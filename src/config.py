from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    KB_PATH: Path = BASE_DIR / "data/knowledge_base.csv"
    PROJECTS_PATH: Path = BASE_DIR / "data/floras_projects.csv"
    FLORAS_BASE_RATE: float = 1.25
    FLORAS_TO_USD: float = 1.0
    DEFAULT_CURRENCY: str = "USD"
    GDP_FALLBACK: float = 0.26
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    VISION_MODEL: str = "gemini-1.5-flash"


settings = Settings()
