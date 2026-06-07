"""
Optional script to regenerate knowledge_base.csv from raw source files.
Run: python -m src.data.seed
"""
from src.config import settings


def seed():
    print(f"Knowledge base path: {settings.KB_PATH}")
    print(f"Data directory: {settings.DATA_DIR}")
    print("Seed script ready. Raw files in data/raw/ can be processed here.")


if __name__ == "__main__":
    seed()
