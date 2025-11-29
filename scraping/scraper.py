import json
from google_play_scraper import app
from fintech.config import RAW_DIR


def fetch_app_metadata(package_id: str):
    """Fetch basic metadata of an Android app."""
    result = app(package_id)
    return {
        "title": result.get("title"),
        "score": result.get("score"),
        "reviews": result.get("reviews"),
        "installs": result.get("installs"),
    }


def save_output(package_id: str, data: dict):
    """Save metadata JSON to output directory."""
    outfile = RAW_DIR / f"{package_id}.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def run_scraper():
    """Run scraper for all defined package IDs."""
    package_ids = [
        "com.combanketh.mobilebanking",
        "com.dasheneBank.consumer",
        "com.boa.boaMobileBanking",
    ]

    for pkg in package_ids:
        metadata = fetch_app_metadata(pkg)
        save_output(pkg, metadata)
        print(f"Saved {pkg}")
