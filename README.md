# Fintech Review Analytics

## Overview
**Fintech Review Analytics** is a Python-based data pipeline designed to **scrape, preprocess, analyze, and visualize user reviews** of Ethiopian banks’ mobile applications.  
It leverages **web scraping, NLP sentiment analysis (VADER), TF-IDF keyword extraction**, and **CI/CD (GitHub Actions)** for automated linting and testing.

###  Key Features
-  Scrape Google Play reviews for Ethiopian bank apps.  
-  Preprocess reviews (deduplicate, normalize dates, validate columns).  
-  Perform sentiment analysis using **VADER**.  
-  Extract keywords & themes using **rule-based mapping + TF-IDF**.  
-  Visualize results in charts & tables.  
-  Automated linting and testing via **GitHub Actions**.  

###  Banks Covered
- **Commercial Bank of Ethiopia (CBE)**  
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**  

---

##  Folder Structure
```text
fintech-review-analytics/
├─ fintech/
│  ├─ __init__.py
│  ├─ config.py
├─ scraping/
│  ├─ __init__.py
│  └─ scraper.py
├─ processing/
│  ├─ __init__.py
│  └─ preprocess.py
├─ sentiment/
│  ├─ __init__.py
│  └─ vader_sentiment.py
├─ scripts/
│  ├─ theme_extraction.py
│  ├─ db_insert.py
│  └─ visualize.py
├─ sql/
│  └─ schema.sql
├─ tests/
│  └─ test_processing.py
├─ .github/
│  └─ workflows/ci.yml
│  └─ PULL_REQUEST_TEMPLATE.md
├─ main.py
├─ helpers.py
├─ requirements.txt
├─ README.md
└─ .env

```

---

##  Getting Started

### 1️. Clone the Repository
```bash
git clone https://github.com/MekdelawitGebre/fintech-review-analytics.git
cd fintech-review-analytics
```

### 2️. Create a Virtual Environment
```bash
python -m venv venv
```
Activate it:

**Windows (PowerShell):**
```bash
venv\Scripts\activate
```
**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3️. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install flake8 pytest vaderSentiment google_play_scraper scikit-learn pandas

```

## 4. .env Setup

Create a `.env` file in the project root to store environment variables:

```bash
touch .env
```

Add the following example variables inside `.env`:

```bash
# Database connection (for storing processed review data)
DATABASE_URL=postgresql://username:password@localhost:5432/fintech_reviews

# Paths and config
DATA_DIR=data
VISUALS_DIR=visuals
LOG_LEVEL=INFO

# Google Play scraping parameters
TARGET_REVIEWS=600
LANGUAGE=en
COUNTRY=us
```

Then, load it in your code using:
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
print("Database URL:", db_url)
```


---

##  Usage

###  1. Preprocess Reviews
```bash
python processing/preprocess.py --in data/raw_reviews.csv --out data/clean_reviews.csv
```
**Output:** Cleaned CSV with columns → `review_id`, `review_text`, `rating`, `date`, `bank`, `source`

###  2. Sentiment Analysis
```bash
python sentiment/vader_sentiment.py --in data/clean_reviews.csv --out data/sentiment_reviews.csv
```
**Output:** CSV with added `vader_score` and `sentiment_label`

###  3. Theme Extraction
```bash
python scripts/theme_extraction.py --in data/sentiment_reviews.csv --out data/annotated_reviews.csv
```
**Output:** Annotated CSV with `themes_list`, `themes`, and top **TF-IDF keywords**

###  4. Scrape New Reviews
```bash
python scraping/scraper.py --target 600 --out data/raw_reviews.csv
```
**Output:** Raw CSV with up to 600 reviews per app

---

##  Running Tests
```bash
pytest -q tests/
```
Set your Python path before testing:

**macOS/Linux**
```bash
export PYTHONPATH=.
```
**Windows PowerShell**
```bash
$env:PYTHONPATH = "."
```

---

##  CI/CD Integration (GitHub Actions)
The CI/CD pipeline (`.github/workflows/ci.yml`) automatically:

1. Sets up Python 3.10  
2. Installs dependencies  
3. Runs **flake8** linting  
4. Executes **pytest** unit tests  
5. Ensures clean, tested code before merging  

---

##  Insights
- **Sentiment Trends:** Understand user satisfaction and frustration points.  
- **Keyword Insights:** Identify recurring themes and improvement areas.  
- **Performance Comparison:** Benchmark banks’ apps by sentiment distribution.  
- **Data-Driven Decisions:** Support UX, marketing, and technical improvements.  

---


