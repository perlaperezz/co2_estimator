from typing import Tuple, Dict, List

CATEGORY_RULES: Dict[str, List[str]] = {
    "Freight": [
        "freight", "shipping", "delivery", "logistics", "courier", "cargo",
        "haulage", "transport", "inbound", "outbound", "parcel", "postage",
        "container", "ocean", "sea freight", "air freight", "trucking",
    ],
    "Travel": [
        "flight", "airfare", "ticket", "hotel", "motel", "lodging",
        "car rental", "taxi", "uber", "lyft", "travel", "mileage",
        "per diem", "expense", "trip", "booking", "accommodation",
    ],
    "Energy": [
        "electricity", "power", "gas", "fuel", "energy", "kwh",
        "utility", "propane", "diesel", "gasoline", "petrol",
        "charging", "grid", "renewable",
    ],
    "Materials": [
        "steel", "concrete", "wood", "lumber", "plastic", "metal",
        "chemical", "raw material", "component", "part", "supply",
        "resin", "alloy", "fabric", "textile", "glass",
    ],
    "Packaging": [
        "packaging", "box", "pallet", "carton", "wrap", "label",
        "bottle", "bag", "container fee", "crate", "strapping",
        "shrink wrap", "tape", "corrugated",
    ],
    "Services": [
        "consulting", "software", "license", "service fee", "support",
        "maintenance", "subscription", "saas", "professional",
        "management fee", "legal", "accounting", "audit", "advisory",
    ],
    "Waste": [
        "waste", "disposal", "recycling", "dump", "landfill",
        "hazardous", "effluent", "scrap removal",
    ],
}


def categorize_item(description: str) -> Tuple[str, str]:
    desc_lower = description.lower()
    scores: Dict[str, int] = {}

    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in desc_lower:
                scores[category] = scores.get(category, 0) + 1

    subcategory_keywords: Dict[str, Dict[str, str]] = {
        "Travel": {"flight": "Air", "airfare": "Air", "ticket": "Air",
                    "hotel": "Hotel", "motel": "Hotel", "lodging": "Hotel",
                    "taxi": "Taxi", "uber": "Taxi", "car rental": "Car"},
        "Energy": {"electricity": "Electricity", "gas": "Natural Gas",
                    "diesel": "Fuel Oil", "petrol": "Fuel Oil", "gasoline": "Fuel Oil"},
        "Freight": {"air": "Air", "ocean": "Sea", "sea": "Sea", "truck": "Road",
                     "van": "Road", "container": "Sea", "rail": "Rail"},
        "Materials": {"steel": "Metal", "concrete": "Construction",
                       "plastic": "Plastic", "wood": "Construction",
                       "paper": "Paper", "metal": "Metal"},
        "Packaging": {"plastic": "Plastic", "paper": "Paper", "wood": "Wood",
                       "box": "Paper", "carton": "Paper", "pallet": "Wood"},
        "Services": {"consulting": "Professional", "software": "Software",
                      "legal": "Professional", "accounting": "Professional"},
    }

    subcategory = ""
    if scores:
        best = max(scores, key=scores.get)
        sub_map = subcategory_keywords.get(best, {})
        for kw, sub in sub_map.items():
            if kw in desc_lower:
                subcategory = sub
                break
        return best, subcategory

    return "General", "GDP-based"


def get_project_category_mapping() -> Dict[str, List[str]]:
    return {
        "Travel": ["Sustainable Aviation Fuel"],
        "Energy": ["Renewable Energy", "Improved Forest Management"],
        "Freight": ["Renewable Energy", "Industrial Process Emissions"],
        "Materials": ["Carbon Mineralization", "Improved Forest Management", "Direct Air Capture"],
        "Packaging": ["Circularity", "Afforestation, Reforestation & Revegetation"],
        "Services": ["Ecosystem Conservation", "Circularity"],
        "Waste": ["Landfill Gas Capture", "Ozone-Depleting Substances Destruction"],
        "General": ["Improved Forest Management", "Carbon Mineralization", "Direct Air Capture"],
    }
