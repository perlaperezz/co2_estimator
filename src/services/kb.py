import pandas as pd
from typing import Optional, Dict, Any, List

from src.config import settings

_kb_df: Optional[pd.DataFrame] = None


def load_kb() -> pd.DataFrame:
    global _kb_df
    if _kb_df is not None:
        return _kb_df
    _kb_df = pd.read_csv(settings.KB_PATH)
    _kb_df["co2_kg"] = pd.to_numeric(_kb_df["co2_kg"], errors="coerce")
    return _kb_df


def query_kb(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
) -> List[Dict[str, Any]]:
    df = load_kb()
    if category:
        df = df[df["category"].str.lower() == category.lower()]
    if subcategory:
        df = df[df["subcategory"].str.lower() == subcategory.lower()]
    return df.to_dict(orient="records")


def find_match(description: str, category_hint: Optional[str] = None) -> Optional[Dict[str, Any]]:
    df = load_kb()
    desc_lower = description.lower()

    if category_hint:
        candidates = df[df["category"].str.lower() == category_hint.lower()]
    else:
        candidates = df

    for _, row in candidates.iterrows():
        item = str(row["item"]).lower()
        if item in desc_lower:
            return row.to_dict()

    for _, row in df.iterrows():
        item = str(row["item"]).lower()
        if item in desc_lower:
            return row.to_dict()

    return None


def get_category_average(category: str) -> Optional[float]:
    df = load_kb()
    sub = df[df["category"].str.lower() == category.lower()]
    if sub.empty:
        return None
    return float(sub["co2_kg"].mean())


def get_gdp_fallback() -> float:
    return settings.GDP_FALLBACK
