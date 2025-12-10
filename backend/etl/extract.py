"""Data extraction from external APIs."""
import praw
import requests
import time
from typing import List, Dict, Any
from datetime import datetime
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.config import Config


class DataExtractor:
    """Extract data from Reddit and News APIs."""
    
    def __init__(self):
        """Initialize extractor with API credentials."""
        self.reddit = None
        self._init_reddit()
    
    def _init_reddit(self):
        """Initialize Reddit API client."""
        if Config.REDDIT_CLIENT_ID and Config.REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=Config.REDDIT_CLIENT_ID,
                client_secret=Config.REDDIT_CLIENT_SECRET,
                user_agent=Config.REDDIT_USER_AGENT
            )
    
    def extract_reddit(self, keyword: str, limit: int = None) -> List[Dict[str, Any]]:
        """Extract posts from Reddit based on keyword.
        
        Args:
            keyword: Technology keyword to search for
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of post data dictionaries
        """
        if not self.reddit:
            return []
        
        limit = limit or Config.REDDIT_LIMIT
        results = []
        
        try:
            # Search in relevant subreddits
            subreddits = ["programming", "webdev", "learnprogramming", "technology"]
            
            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    posts = subreddit.search(keyword, limit=limit, sort="hot", time_filter="week")
                    
                    for post in posts:
                        if keyword.lower() in post.title.lower() or keyword.lower() in post.selftext.lower():
                            results.append({
                                "title": post.title,
                                "content": post.selftext[:1000] if post.selftext else post.title,  # Limit content length
                                "source": "reddit",
                                "url": f"https://reddit.com{post.permalink}",
                                "timestamp": datetime.fromtimestamp(post.created_utc).isoformat(),
                                "keyword": keyword
                            })
                            
                            if len(results) >= limit:
                                break
                    
                    if len(results) >= limit:
                        break
                    
                    # Rate limiting
                    time.sleep(1)
                except Exception as e:
                    print(f"Error extracting from r/{subreddit_name}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error in Reddit extraction: {e}")
        
        return results[:limit]
    
    def extract_news(self, keyword: str, limit: int = None) -> List[Dict[str, Any]]:
        """Extract articles from News API based on keyword.
        
        Args:
            keyword: Technology keyword to search for
            limit: Maximum number of articles to retrieve
            
        Returns:
            List of article data dictionaries
        """
        if not Config.NEWS_API_KEY:
            return []
        
        limit = limit or Config.NEWS_LIMIT
        results = []
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": keyword,
                "apiKey": Config.NEWS_API_KEY,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "ok":
                for article in data.get("articles", [])[:limit]:
                    if article.get("title") and article.get("content"):
                        results.append({
                            "title": article.get("title", ""),
                            "content": article.get("content", "")[:1000] if article.get("content") else article.get("description", "")[:1000],
                            "source": "news",
                            "url": article.get("url", ""),
                            "timestamp": article.get("publishedAt", datetime.now().isoformat()),
                            "keyword": keyword
                        })
        
        except requests.exceptions.RequestException as e:
            print(f"Error in News API extraction: {e}")
        except Exception as e:
            print(f"Unexpected error in News extraction: {e}")
        
        return results
    
    def extract_all(self, keywords: List[str] = None) -> List[Dict[str, Any]]:
        """Extract data for all keywords from all sources.
        
        Args:
            keywords: List of keywords to extract. Defaults to Config.KEYWORDS.
            
        Returns:
            List of all extracted data
        """
        keywords = keywords or Config.KEYWORDS
        all_data = []
        
        for keyword in keywords:
            print(f"Extracting data for keyword: {keyword}")
            
            # Extract from Reddit
            reddit_data = self.extract_reddit(keyword)
            all_data.extend(reddit_data)
            
            # Extract from News
            news_data = self.extract_news(keyword)
            all_data.extend(news_data)
            
            # Rate limiting between keywords
            time.sleep(2)
        
        return all_data

