"""Compute VADER sentiment scores and labels for cleaned reviews."""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from fintech.config import DATA_DIR
from helpers import logger
import argparse


def annotate_sentiment(in_csv: str, out_csv: str):
    """Annotate cleaned reviews with VADER sentiment scores and labels."""
    logger.info("Loading cleaned reviews: %s", in_csv)
    df = pd.read_csv(in_csv, dtype={"review_id": str, "review_text": str})

    analyzer = SentimentIntensityAnalyzer()
    logger.info("Scoring %d reviews", len(df))

    # Compute compound sentiment scores
    scores = df["review_text"].astype(str).apply(
        lambda t: analyzer.polarity_scores(t)["compound"]
    )

    # Map scores to sentiment labels
    labels = scores.apply(
        lambda s: "positive" if s > 0.05 else ("negative" if s < -0.05 else "neutral")
    )

    df["vader_score"] = scores
    df["sentiment_label"] = labels

    # Save annotated CSV
    df.to_csv(out_csv, index=False, encoding="utf-8")
    logger.info("Saved sentiment annotated CSV to %s", out_csv)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute VADER sentiment scores and labels for cleaned reviews."
    )
    parser.add_argument(
        "--in",
        dest="in_csv",
        default=str(DATA_DIR / "clean_reviews.csv"),
        help="Input CSV file containing cleaned reviews",
    )
    parser.add_argument(
        "--out",
        dest="out_csv",
        default=str(DATA_DIR / "sentiment_reviews.csv"),
        help="Output CSV file with sentiment scores and labels",
    )
    args = parser.parse_args()
    annotate_sentiment(args.in_csv, args.out_csv)
