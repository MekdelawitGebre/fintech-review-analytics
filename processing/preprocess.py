"""Preprocess scraped reviews: dedupe, drop missing, normalize date, ensure columns."""
import pandas as pd
from fintech.config import DATA_DIR
from helpers import logger
import argparse


REQUIRED_COLS = ["bank", "review_id", "review", "rating", "date", "source"]


def preprocess(in_csv: str, out_csv: str):
    logger.info("Loading raw csv: %s", in_csv)
    df = pd.read_csv(in_csv, dtype={"review_id": str, "review": str})
    # ensure required columns if date was scraped; if not, we try to read 'date' or 'at'
    # standardize column names if needed
    if "at" in df.columns and "date" not in df.columns:
        df["date"] = pd.to_datetime(df["at"]).dt.strftime("%Y-%m-%d")
    # drop empties
    before = len(df)
    df = df[df["review"].notna() & (df["review"].str.strip() != "")]
    # dedupe on bank+review_id or bank+review text
    if "review_id" in df.columns and df["review_id"].notna().any():
        df = df.drop_duplicates(subset=["bank", "review_id"])
    else:
        df = df.drop_duplicates(subset=["bank", "review"])
    # normalize date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    else:
        df["date"] = pd.NaT
    after = len(df)
    logger.info("Preprocess: before=%d after=%d dropped=%d", before, after, before - after)
    # output columns as requested
    out_df = df.rename(columns={"review": "review_text", "rating": "rating"})
    out_df = out_df[["review_id", "review_text", "rating", "date", "bank", "source"]]
    out_df.to_csv(out_csv, index=False, encoding="utf-8")
    logger.info("Saved clean CSV to %s (%d rows)", out_csv, len(out_df))
    return out_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_csv", default=str(DATA_DIR / "raw_reviews.csv"))
    parser.add_argument("--out", dest="out_csv", default=str(DATA_DIR / "clean_reviews.csv"))
    args = parser.parse_args()
    preprocess(args.in_csv, args.out_csv)
