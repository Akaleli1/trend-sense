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
        # Config'den gelen yolu kullan veya varsayılanı ayarla
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

    def insert_sentiment(
        self,
        keyword: str,
        source: str,
        title: str,
        content: str,
        url: str,
        sentiment_score: float,
        summary: str
    ) -> bool:
        """Insert a sentiment record into the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO sentiments 
                    (keyword, source, title, content, url, sentiment_score, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (keyword, source, title, content, url, sentiment_score, summary)
                )
                return True
        except sqlite3.IntegrityError:
            # Duplicate URL - bu hatayı yutuyoruz, sorun değil
            return False
        except Exception as e:
            print(f"❌ Veri ekleme hatası: {e}")
            return False
    
    def get_recent_sentiments(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent sentiment records from the database."""
        # Frontend 'sentiment' bekliyor ama DB'de 'sentiment_score' var. Alias (as) kullanıyoruz.
        query = """
            SELECT 
                id,
                keyword,
                source,
                title,
                content,
                url,
                sentiment_score as sentiment, 
                summary,
                created_at
            FROM sentiments 
            ORDER BY created_at DESC 
            LIMIT ?
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Veri çekme hatası: {e}")
            return []

    def get_keywords(self) -> List[str]:
        """Get all unique keywords from the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT keyword FROM sentiments ORDER BY keyword")
                return [row[0] for row in cursor.fetchall()]
        except:
            return []
            
    def get_stats(self, keyword: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for sentiments."""
        query = "SELECT COUNT(*) as count, AVG(sentiment_score) as avg_score FROM sentiments WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND keyword = ?"
            params.append(keyword)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            return {
                "total_count": row[0] if row else 0,
                "average_sentiment": round(row[1], 3) if row and row[1] else 0.0
            }
    
    def get_advanced_stats(self) -> Dict[str, Any]:
        """Get advanced statistics including top and bottom keywords."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total articles count
                cursor.execute("SELECT COUNT(*) FROM sentiments")
                total_articles = cursor.fetchone()[0] or 0
                
                # Average sentiment
                cursor.execute("SELECT AVG(sentiment_score) FROM sentiments")
                avg_result = cursor.fetchone()[0]
                average_sentiment = round(avg_result, 3) if avg_result else 0.0
                
                # Top 3 keywords with highest average sentiment
                cursor.execute("""
                    SELECT keyword, AVG(sentiment_score) as avg_sentiment
                    FROM sentiments
                    GROUP BY keyword
                    HAVING COUNT(*) > 0
                    ORDER BY avg_sentiment DESC
                    LIMIT 3
                """)
                top_rows = cursor.fetchall()
                top_keywords = [
                    {"keyword": row[0], "avg_sentiment": round(row[1], 3)}
                    for row in top_rows
                ]
                
                # Bottom 3 keywords with lowest average sentiment
                cursor.execute("""
                    SELECT keyword, AVG(sentiment_score) as avg_sentiment
                    FROM sentiments
                    GROUP BY keyword
                    HAVING COUNT(*) > 0
                    ORDER BY avg_sentiment ASC
                    LIMIT 3
                """)
                bottom_rows = cursor.fetchall()
                bottom_keywords = [
                    {"keyword": row[0], "avg_sentiment": round(row[1], 3)}
                    for row in bottom_rows
                ]
                
                return {
                    "total_articles": total_articles,
                    "average_sentiment": average_sentiment,
                    "top_keywords": top_keywords,
                    "bottom_keywords": bottom_keywords
                }
        except Exception as e:
            print(f"❌ Advanced stats error: {e}")
            return {
                "total_articles": 0,
                "average_sentiment": 0.0,
                "top_keywords": [],
                "bottom_keywords": []
            }