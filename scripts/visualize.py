"""Produce simple plots: sentiment distribution per bank, rating distribution, top negative words."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fintech.config import VIS_DIR, DATA_DIR
from helpers import logger
from sklearn.feature_extraction.text import CountVectorizer
import argparse

sns.set(style="whitegrid")


def plot_sentiment_by_bank(df, out_path):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="bank", hue="sentiment_label")
    plt.title("Sentiment distribution by bank")
    plt.xlabel("Bank")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info("Saved %s", out_path)


def plot_rating_distribution(df, out_path):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="rating", hue="bank")
    plt.title("Rating distribution by bank")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info("Saved %s", out_path)


def plot_top_negative_words(df, out_path):
    neg = df[df["sentiment_label"] == "negative"]["review_text"].astype(str)
    if neg.empty:
        logger.warning("No negative reviews to analyze for word frequency.")
        return
    vec = CountVectorizer(stop_words="english", max_features=20)
    X = vec.fit_transform(neg)
    counts = X.toarray().sum(axis=0)
    words = vec.get_feature_names_out()
    order = counts.argsort()[::-1]
    plt.figure(figsize=(8, 6))
    sns.barplot(x=counts[order], y=[words[i] for i in order])
    plt.title("Top words in negative reviews")
    plt.xlabel("Frequency")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    logger.info("Saved %s", out_path)


def main(in_csv: str, out_dir: str):
    logger.info("Loading annotated data: %s", in_csv)
    df = pd.read_csv(in_csv)
    plot_sentiment_by_bank(df, f"{out_dir}/sentiment_by_bank.png")
    plot_rating_distribution(df, f"{out_dir}/rating_distribution.png")
    plot_top_negative_words(df, f"{out_dir}/top_negative_words.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_csv", default=str(DATA_DIR / "annotated_reviews.csv"))
    parser.add_argument("--out", dest="out_dir", default=str(VIS_DIR))
    args = parser.parse_args()
    main(args.in_csv, args.out_dir)
