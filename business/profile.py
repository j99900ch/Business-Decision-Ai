"""
Business DecisionAI
Business Profile Management

This module is isolated from the existing Streamlit application.
It stores the identity and basic information of a business.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re


@dataclass
class BusinessProfile:
    company_id: str
    company_name: str
    industry: str = ""
    products: str = ""
    market: str = ""
    location: str = ""


def create_company_id(company_name: str) -> str:
    """
    Convert a company name into a safe internal ID.
    """

    cleaned = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        company_name.strip().upper()
    )

    cleaned = cleaned.strip("_")

    if not cleaned:
        raise ValueError("Company name cannot be empty.")

    return cleaned


def create_profile(
    company_name: str,
    industry: str = "",
    products: str = "",
    market: str = "",
    location: str = "",
) -> BusinessProfile:

    if not company_name.strip():
        raise ValueError("Company name is required.")

    company_id = create_company_id(company_name)

    return BusinessProfile(
        company_id=company_id,
        company_name=company_name.strip(),
        industry=industry.strip(),
        products=products.strip(),
        market=market.strip(),
        location=location.strip(),
    )


def save_profile(
    profile: BusinessProfile,
    base_directory: str = "data/companies",
) -> str:

    company_directory = (
        Path(base_directory) / profile.company_id
    )

    company_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    profile_path = company_directory / "profile.json"

    with open(
        profile_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            asdict(profile),
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(profile_path)


def load_profile(
    company_id: str,
    base_directory: str = "data/companies",
) -> BusinessProfile:

    profile_path = (
        Path(base_directory)
        / company_id
        / "profile.json"
    )

    if not profile_path.exists():
        raise FileNotFoundError(
            f"No business profile found for: {company_id}"
        )

    with open(
        profile_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return BusinessProfile(**data)