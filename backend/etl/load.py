"""Data loading into SQLite database."""
from typing import List, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.database.db import Database
from backend.models.sentiment import SentimentRecord


class DataLoader:
    """Load transformed data into the database."""
    
    def __init__(self, db: Database = None):
        """Initialize data loader.
        
        Args:
            db: Database instance. Creates new one if not provided.
        """
        self.db = db or Database()
    
    def load_record(self, record: Dict[str, Any]) -> bool:
        """Load a single record into the database.
        
        Args:
            record: Dictionary containing sentiment data
            
        Returns:
            True if loaded successfully, False if duplicate or error
        """
        try:
            sentiment_record = SentimentRecord(
                keyword=record.get("keyword", ""),
                source=record.get("source", ""),
                title=record.get("title", ""),
                content=record.get("content", ""),
                url=record.get("url", ""),
                sentiment_score=float(record.get("sentiment_score", 0.0)),
                summary=record.get("summary", "")
            )
            
            if not sentiment_record.validate():
                print(f"Invalid record: {sentiment_record.title}")
                return False
            
            return self.db.insert_sentiment(
                keyword=sentiment_record.keyword,
                source=sentiment_record.source,
                title=sentiment_record.title,
                content=sentiment_record.content,
                url=sentiment_record.url,
                sentiment_score=sentiment_record.sentiment_score,
                summary=sentiment_record.summary
            )
        
        except Exception as e:
            print(f"Error loading record: {e}")
            return False
    
    def load_batch(self, records: List[Dict[str, Any]]) -> Dict[str, int]:
        """Load a batch of records into the database.
        
        Args:
            records: List of record dictionaries
            
        Returns:
            Dictionary with counts: loaded, duplicates, errors
        """
        stats = {
            "loaded": 0,
            "duplicates": 0,
            "errors": 0
        }
        
        for record in records:
            try:
                success = self.load_record(record)
                if success:
                    stats["loaded"] += 1
                else:
                    stats["duplicates"] += 1
            except Exception as e:
                print(f"Error in batch load: {e}")
                stats["errors"] += 1
        
        return stats

