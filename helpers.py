import json
import logging


def load_json(path: str):
    """Load JSON file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data):
    """Save dictionary as JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)