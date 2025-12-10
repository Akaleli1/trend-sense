"""Data models for sentiment analysis."""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class SentimentRecord:
    """Represents a sentiment analysis record."""
    
    keyword: str
    source: str
    title: str
    content: str
    url: str
    sentiment_score: float
    summary: str
    created_at: Optional[datetime] = None
    id: Optional[int] = None
    
    def validate(self) -> bool:
        """Validate the sentiment record."""
        if not (-1.0 <= self.sentiment_score <= 1.0):
            return False
        if not self.keyword or not self.source:
            return False
        return True

