# helpers.py
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def ensure_cols(df, required_cols):
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
    return df


def some_helper_function():  # Example function
    pass
