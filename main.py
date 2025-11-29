"""Run the full pipeline end-to-end. Use cautiously: scraping may take time and DB insertion requires DB URL."""
from scraping.scraper import main as scrape_main
from processing.preprocess import preprocess
from sentiment.vader_sentiment import annotate_sentiment
from scripts.theme_extraction import annotate_themes
from scripts.db_insert import upsert_into_db
from scripts.visualize import main as visualize_main
from fintech.config import DATA_DIR
from helpers import logger
from pathlib import Path

RAW_CSV = str(DATA_DIR / "raw_reviews.csv")
CLEAN_CSV = str(DATA_DIR / "clean_reviews.csv")
SENTIMENT_CSV = str(DATA_DIR / "sentiment_reviews.csv")
ANNOTATED_CSV = str(DATA_DIR / "annotated_reviews.csv")
VIS_DIR = str(Path.cwd() / "visuals")


def run_all(target_each: int = 600):
    logger.info("Starting full pipeline")
    # 1. Scrape
    scrape_main(target_each=target_each, out_csv=RAW_CSV)
    # 2. Preprocess
    preprocess(RAW_CSV, CLEAN_CSV)
    # 3. Sentiment
    annotate_sentiment(CLEAN_CSV, SENTIMENT_CSV)
    # 4. Themes
    annotate_themes(SENTIMENT_CSV, ANNOTATED_CSV)
    # 5. DB insert (requires DATABASE_URL in .env)
    try:
        upsert_into_db(ANNOTATED_CSV)
    except Exception as e:
        logger.exception("DB insertion failed: %s", e)
    # 6. Visualize
    visualize_main(ANNOTATED_CSV, VIS_DIR)
    logger.info("Pipeline finished")


if __name__ == "__main__":
    run_all(target_each=600)
