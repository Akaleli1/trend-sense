-- Database schema for Tech Trend Sentiment Analyst

CREATE TABLE IF NOT EXISTS sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    source TEXT NOT NULL,
    title TEXT,
    content TEXT,
    url TEXT UNIQUE,
    sentiment_score REAL NOT NULL,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_keyword_date ON sentiments(keyword, created_at);
CREATE INDEX IF NOT EXISTS idx_source ON sentiments(source);
CREATE INDEX IF NOT EXISTS idx_created_at ON sentiments(created_at);

