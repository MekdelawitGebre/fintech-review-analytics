"""Preprocess scraped reviews: dedupe, drop missing, normalize date,
ensure columns. """

import argparse
import pandas as pd
from fintech.config import DATA_DIR
from helpers import logger

REQUIRED_COLS = ["bank", "review_id", "review", "rating", "date", "source"]


def preprocess(in_csv: str, out_csv: str):
    """Load, clean, deduplicate, normalize dates, and save reviews."""
    logger.info("Loading raw csv: %s", in_csv)
    df = pd.read_csv(in_csv, dtype={"review_id": str, "review": str})

    # Standardize date column if 'at' exists
    if "at" in df.columns and "date" not in df.columns:
        df["date"] = pd.to_datetime(df["at"]).dt.strftime("%Y-%m-%d")

    # Drop empty reviews
    before = len(df)
    df = df[df["review"].notna() & (df["review"].str.strip() != "")]

    # Deduplicate on bank+review_id or bank+review text
    if "review_id" in df.columns and df["review_id"].notna().any():
        df = df.drop_duplicates(subset=["bank", "review_id"])
    else:
        df = df.drop_duplicates(subset=["bank", "review"])

    # Normalize date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    else:
        df["date"] = pd.NaT

    after = len(df)
    logger.info(
        "Preprocess: before=%d after=%d dropped=%d",
        before,
        after,
        before - after,
    )

    # Rename and reorder columns
    out_df = df.rename(columns={"review": "review_text"})
    out_df = out_df[
        ["review_id", "review_text", "rating", "date", "bank", "source"]
    ]

    # Save cleaned CSV
    out_df.to_csv(out_csv, index=False, encoding="utf-8")
    logger.info(
        "Saved clean CSV to %s (%d rows)",
        out_csv,
        len(out_df),
    )

    return out_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--in",
        dest="in_csv",
        default=str(DATA_DIR / "raw_reviews.csv"),
        help="Input CSV file path",
    )
    parser.add_argument(
        "--out",
        dest="out_csv",
        default=str(DATA_DIR / "clean_reviews.csv"),
        help="Output CSV file path",
    )
    args = parser.parse_args()
    preprocess(args.in_csv, args.out_csv)
