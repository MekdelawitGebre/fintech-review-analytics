"""Extract keywords/themes using TF-IDF and a rule-based theme map."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from fintech.config import DATA_DIR
from helpers import logger
import argparse
import re


THEME_KEYWORDS = {
    "Account Access": ["login", "signin", "password", "otp", "fingerprint", "biometric", "pin"],
    "Transactions": ["transfer", "send", "payment", "transaction", "pending", "failed", "confirm"],
    "Performance": ["slow", "lag", "loading", "crash", "crashes", "timeout", "delay"],
    "UI/UX": ["ui", "interface", "button", "navigation", "design", "easy to use", "ux"],
    "Support": ["support", "customer", "help", "agent", "call", "chat", "service"],
}


def detect_themes_rule(text: str):
    t = str(text).lower()
    hits = []
    for theme, keys in THEME_KEYWORDS.items():
        for k in keys:
            if k in t:
                hits.append(theme)
                break
    if not hits:
        hits = ["Other"]
    return hits


def extract_tfidf_candidates(corpus, top_k=10):
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=500)
    mat = vec.fit_transform(corpus)
    # compute average tfidf per term
    import numpy as np

    avg_scores = mat.mean(axis=0).A1
    terms = vec.get_feature_names_out()
    scored = sorted(zip(terms, avg_scores), key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def annotate_themes(in_csv: str, out_csv: str):
    logger.info("Loading sentiment csv: %s", in_csv)
    df = pd.read_csv(in_csv, dtype={"review_text": str})
    # rule-based mapping
    logger.info("Applying rule-based theme detection")
    df["themes_list"] = df["review_text"].apply(detect_themes_rule)
    df["themes"] = df["themes_list"].apply(lambda lst: ",".join(lst))
    # optional: aggregate top tf-idf candidates for reporting
    logger.info("Computing TF-IDF candidate terms")
    top_terms = extract_tfidf_candidates(df["review_text"].astype(str).tolist(), top_k=50)
    logger.info("Top TF-IDF candidates: %s", ", ".join([t for t, _ in top_terms[:10]]))
    df.to_csv(out_csv, index=False, encoding="utf-8")
    logger.info("Saved annotated reviews (themes) to %s", out_csv)
    return df, top_terms


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_csv", default=str(DATA_DIR / "sentiment_reviews.csv"))
    parser.add_argument("--out", dest="out_csv", default=str(DATA_DIR / "annotated_reviews.csv"))
    args = parser.parse_args()
    annotate_themes(args.in_csv, args.out_csv)
