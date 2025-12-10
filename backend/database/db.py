"""Database connection and utility functions."""
import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.config import Config


class Database:
    """Database connection manager."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. Defaults to Config.DATABASE_PATH.
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self._ensure_db_directory()
        self._initialize_schema()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def _initialize_schema(self):
        """Initialize database schema from schema.sql."""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "database",
            "schema.sql"
        )
        
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            with self.get_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()
    
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
        """Insert a sentiment record into the database.
        
        Args:
            keyword: Technology keyword
            source: Data source (reddit, news)
            title: Article/post title
            content: Article/post content
            url: Source URL
            sentiment_score: Sentiment score (-1.0 to 1.0)
            summary: AI-generated summary
            
        Returns:
            True if inserted, False if duplicate
        """
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
            # Duplicate URL
            return False
    
    def get_sentiments(
        self,
        keyword: Optional[str] = None,
        source: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query sentiments from the database.
        
        Args:
            keyword: Filter by keyword
            source: Filter by source
            start_date: Filter by start date (YYYY-MM-DD)
            end_date: Filter by end date (YYYY-MM-DD)
            limit: Maximum number of results
            
        Returns:
            List of sentiment records as dictionaries
        """
        query = "SELECT * FROM sentiments WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND keyword = ?"
            params.append(keyword)
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        if start_date:
            query += " AND DATE(created_at) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(created_at) <= ?"
            params.append(end_date)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_keywords(self) -> List[str]:
        """Get all unique keywords from the database.
        
        Returns:
            List of unique keywords
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT keyword FROM sentiments ORDER BY keyword")
            return [row[0] for row in cursor.fetchall()]
    
    def get_stats(self, keyword: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for sentiments.
        
        Args:
            keyword: Filter by keyword (optional)
            
        Returns:
            Dictionary with statistics
        """
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

