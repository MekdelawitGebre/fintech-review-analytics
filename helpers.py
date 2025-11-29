import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def ensure_cols(df, cols):
    for c in cols:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")
    return True
