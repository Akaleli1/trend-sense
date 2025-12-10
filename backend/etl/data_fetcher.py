"""Helper functions to fetch data from external APIs and return structured data."""
import os
import requests
import random
from typing import List, Dict, Any
from datetime import datetime
from backend.config import Config


def fetch_hacker_news_data(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch data from Hacker News API.
    
    Args:
        keyword: Technology keyword to search for
        limit: Maximum number of results to return
        
    Returns:
        List of dictionaries with title, content, url, source, and sentiment
    """
    results = []
    
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            for item in data.get('hits', [])[:limit]:
                # Generate dummy sentiment score (will be replaced with AI later)
                sentiment = round(random.uniform(-1.0, 1.0), 2)
                
                results.append({
                    'title': item.get('title', ''),
                    'content': item.get('story_text', '') or item.get('title', ''),
                    'url': item.get('url', f"https://news.ycombinator.com/item?id={item.get('objectID', '')}"),
                    'source': 'hackernews',
                    'keyword': keyword,
                    'sentiment': sentiment,
                    'created_at': datetime.fromtimestamp(item.get('created_at_i', 0)).isoformat() if item.get('created_at_i') else datetime.now().isoformat()
                })
    except Exception as e:
        print(f"Error fetching Hacker News data: {e}")
    
    return results


def fetch_news_api_data(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch data from News API.
    
    Args:
        keyword: Technology keyword to search for
        limit: Maximum number of results to return
        
    Returns:
        List of dictionaries with title, content, url, source, and sentiment
    """
    results = []
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        print("Warning: NEWS_API_KEY not found. Skipping News API fetch.")
        return results
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': keyword,
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('totalResults', 0) > 0:
                for item in data.get('articles', [])[:limit]:
                    # Generate dummy sentiment score (will be replaced with AI later)
                    sentiment = round(random.uniform(-1.0, 1.0), 2)
                    
                    results.append({
                        'title': item.get('title', ''),
                        'content': item.get('content', '') or item.get('description', ''),
                        'url': item.get('url', ''),
                        'source': 'news',
                        'keyword': keyword,
                        'sentiment': sentiment,
                        'created_at': item.get('publishedAt', datetime.now().isoformat())
                    })
    except Exception as e:
        print(f"Error fetching News API data: {e}")
    
    return results


def fetch_all_trends_data(keywords: List[str] = None) -> List[Dict[str, Any]]:
    """Fetch data for all keywords from all sources.
    
    Args:
        keywords: List of keywords to fetch. Defaults to Config.KEYWORDS.
        
    Returns:
        List of all fetched data with sentiment scores
    """
    keywords = keywords or Config.KEYWORDS
    all_data = []
    
    for keyword in keywords:
        # Fetch from Hacker News
        hn_data = fetch_hacker_news_data(keyword, limit=5)
        all_data.extend(hn_data)
        
        # Fetch from News API
        news_data = fetch_news_api_data(keyword, limit=5)
        all_data.extend(news_data)
    
    return all_data

