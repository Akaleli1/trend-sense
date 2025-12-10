"""Configuration management for the application."""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "TrendSense/1.0")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/sentiments.db")
    
    # Flask
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_HOST: str = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Keywords
    KEYWORDS: List[str] = [
        keyword.strip() 
        for keyword in os.getenv("KEYWORDS", "Next.js,TypeScript,AI,React,Python").split(",")
    ]
    
    # ETL Settings
    REDDIT_LIMIT: int = int(os.getenv("REDDIT_LIMIT", "10"))
    NEWS_LIMIT: int = int(os.getenv("NEWS_LIMIT", "10"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required = [
            cls.GEMINI_API_KEY,
            cls.REDDIT_CLIENT_ID,
            cls.REDDIT_CLIENT_SECRET,
            cls.NEWS_API_KEY,
        ]
        return all(required)
    
    @classmethod
    def get_missing_config(cls) -> List[str]:
        """Get list of missing configuration keys."""
        missing = []
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not cls.REDDIT_CLIENT_ID:
            missing.append("REDDIT_CLIENT_ID")
        if not cls.REDDIT_CLIENT_SECRET:
            missing.append("REDDIT_CLIENT_SECRET")
        if not cls.NEWS_API_KEY:
            missing.append("NEWS_API_KEY")
        return missing

