"""Scrape Google Play reviews using google_play_scraper."""
from google_play_scraper import reviews, Sort, reviews_all
import pandas as pd
from fintech.config import RAW_DIR, DATA_DIR
from helpers import logger
import argparse
import time


APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking", 
    "Dashen": "com.dashen.dashensuperapp"      
}


def scrape_app(pkg_name: str, bank_name: str, target: int = 600, lang="en", country="us"):
    logger.info("Scraping %s (%s) target=%d", bank_name, pkg_name, target)
    out = []
    # use reviews_all which fetches many; slice to target
    try:
        all_reviews = reviews_all(pkg_name, lang=lang, country=country)
    except Exception as e:
        logger.exception("Failed to fetch all reviews for %s: %s", bank_name, e)
        # fallback: try paginated reviews
        all_reviews = []
    if not all_reviews:
        logger.warning("No reviews returned for %s. Returning empty list.", bank_name)
        return out
    count = 0
    for r in all_reviews:
        out.append(
            {
                "bank": bank_name,
                "review_id": r.get("reviewId"),
                "review": r.get("content") or "",
                "rating": r.get("score"),
                "date": r.get("at").isoformat() if r.get("at") else None,
                "source": "google_play",
            }
        )
        count += 1
        if count >= target:
            break
        # polite pause occasionally
        if count % 200 == 0:
            time.sleep(1)
    logger.info("Collected %d reviews for %s", len(out), bank_name)
    return out


def main(target_each: int = 600, out_csv: str = None):
    rows = []
    for bank, pkg in APPS.items():
        data = scrape_app(pkg, bank, target=target_each)
        rows.extend(data)
    df = pd.DataFrame(rows)
    if out_csv is None:
        out_csv = DATA_DIR / "raw_reviews.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")
    logger.info("Saved raw reviews to %s (%d rows)", out_csv, len(df))
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Google Play reviews for target apps.")
    parser.add_argument("--target", type=int, default=600, help="Target reviews per app (default 600)")
    parser.add_argument("--out", type=str, default=str(DATA_DIR / "raw_reviews.csv"), help="Output CSV path")
    args = parser.parse_args()
    main(target_each=args.target, out_csv=args.out)
