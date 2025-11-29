CREATE TABLE IF NOT EXISTS banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name TEXT UNIQUE NOT NULL,
  app_package TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id TEXT PRIMARY KEY,
  bank_id INTEGER REFERENCES banks(bank_id),
  review_text TEXT,
  rating SMALLINT,
  review_date DATE,
  sentiment_label TEXT,
  sentiment_score REAL,
  themes TEXT,
  source TEXT,
  ingested_at TIMESTAMP DEFAULT now()
);
