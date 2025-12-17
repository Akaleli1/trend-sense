"""Database connection and utility functions."""
import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from datetime import datetime
from config import Config

class Database:
    """Database connection manager."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = db_path or os.path.join(base_dir, "data", "sentiments.db")
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            source TEXT NOT NULL,
            title TEXT,
            content TEXT,
            url TEXT UNIQUE,
            sentiment_score REAL,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self.get_connection() as conn:
                conn.execute(query)
            print(f"✅ Tablolar başarıyla oluşturuldu/kontrol edildi: {self.db_path}")
        except Exception as e:
            print(f"❌ Tablo oluşturma hatası: {e}")

    # --- YENİ EKLENEN AKILLI KONTROL FONKSİYONU ---
    def check_if_url_exists(self, url: str) -> bool:
        """Check if a URL already exists in the database to avoid re-analysis."""
        query = "SELECT 1 FROM sentiments WHERE url = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (url,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking URL: {e}")
            return False
    # ----------------------------------------------

    def insert_sentiment(self, keyword: str, source: str, title: str, content: str, url: str, sentiment_score: float, summary: str) -> bool:
        """Insert a sentiment record."""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO sentiments (keyword, source, title, content, url, sentiment_score, summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (keyword, source, title, content, url, sentiment_score, summary)
                )
                return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"❌ Veri ekleme hatası: {e}")
            return False

    def get_sentiments(self, keyword=None, source=None, start_date=None, end_date=None, limit=None) -> List[Dict[str, Any]]:
        """Query sentiments with filters."""
        query = "SELECT * FROM sentiments WHERE 1=1"
        params = []
        if keyword:
            query += " AND keyword = ?"; params.append(keyword)
        if source:
            query += " AND source = ?"; params.append(source)
        if start_date:
            query += " AND DATE(created_at) >= ?"; params.append(start_date)
        if end_date:
            query += " AND DATE(created_at) <= ?"; params.append(end_date)
        query += " ORDER BY created_at DESC"
        if limit:
            query += " LIMIT ?"; params.append(limit)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception: return []

    def get_recent_sentiments(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent sentiment records."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, keyword, source, title, content, url, sentiment_score as sentiment, summary, created_at FROM sentiments ORDER BY created_at DESC LIMIT ?", (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception: return []

    def get_keywords(self) -> List[str]:
        """Get unique keywords."""
        try:
            with self.get_connection() as conn:
                return [row[0] for row in conn.execute("SELECT DISTINCT keyword FROM sentiments ORDER BY keyword").fetchall()]
        except: return []

    def get_advanced_stats(self) -> Dict[str, Any]:
        """Get advanced stats."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                total = cursor.execute("SELECT COUNT(*) FROM sentiments").fetchone()[0] or 0
                avg = cursor.execute("SELECT AVG(sentiment_score) FROM sentiments").fetchone()[0]
                avg_sentiment = round(avg, 2) if avg else 0.0
                
                top = [{"keyword": r[0], "avg_sentiment": round(r[1], 2)} for r in cursor.execute("SELECT keyword, AVG(sentiment_score) as a FROM sentiments GROUP BY keyword ORDER BY a DESC LIMIT 3").fetchall()]
                bottom = [{"keyword": r[0], "avg_sentiment": round(r[1], 2)} for r in cursor.execute("SELECT keyword, AVG(sentiment_score) as a FROM sentiments GROUP BY keyword ORDER BY a ASC LIMIT 3").fetchall()]
                
                return {"total_articles": total, "average_sentiment": avg_sentiment, "top_keywords": top, "bottom_keywords": bottom}
        except Exception: return {"total_articles": 0, "average_sentiment": 0.0, "top_keywords": [], "bottom_keywords": []}