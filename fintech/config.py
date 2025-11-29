from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"
VIS_DIR = BASE_DIR / "visuals"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL")
