"""Insert annotated CSV rows into Neon Postgres. Uses DATABASE_URL from .env."""
import os
import csv
import argparse
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_batch
from helpers import logger
from fintech.config import DATA_DIR
from pathlib import Path

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL not set. Copy .env.example to .env and fill.")
    raise RuntimeError("DATABASE_URL not set.")

SCHEMA_SQL = Path("sql/schema.sql")


def upsert_into_db(csv_path: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # apply schema
    with open(SCHEMA_SQL, "r", encoding="utf-8") as fh:
        cur.execute(fh.read())
    conn.commit()
    logger.info("Ensured DB schema applied.")
    # read csv rows
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    # upsert banks
    banks = sorted(list({r["bank"] for r in rows if r.get("bank")}))
    for b in banks:
        cur.execute(
            "INSERT INTO banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING",
            (b,),
        )
    conn.commit()
    cur.execute("SELECT bank_id, bank_name FROM banks")
    bank_map = {name: bid for (bid, name) in [(row[0], row[1]) for row in cur.fetchall()]}
    logger.info("Banks upserted: %s", ", ".join(banks))
    # insert reviews in batch
    insert_q = """
    INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, themes, source)
    VALUES (%(review_id)s, %(bank_id)s, %(review_text)s, %(rating)s, %(review_date)s, %(sentiment_label)s, %(sentiment_score)s, %(themes)s, %(source)s)
    ON CONFLICT (review_id) DO NOTHING
    """
    params = []
    for r in rows:
        params.append(
            {
                "review_id": r.get("review_id"),
                "bank_id": bank_map.get(r.get("bank")),
                "review_text": r.get("review_text") or r.get("review") or "",
                "rating": int(r.get("rating")) if r.get("rating") else None,
                "review_date": r.get("date"),
                "sentiment_label": r.get("sentiment_label"),
                "sentiment_score": float(r.get("vader_score")) if r.get("vader_score") else None,
                "themes": r.get("themes") or r.get("themes_str") or "",
                "source": r.get("source", "google_play"),
            }
        )
    execute_batch(cur, insert_q, params, page_size=100)
    conn.commit()
    logger.info("Inserted %d rows into reviews table (duplicates skipped)", len(params))
    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_csv", default=str(DATA_DIR / "annotated_reviews.csv"))
    args = parser.parse_args()
    upsert_into_db(args.in_csv)
