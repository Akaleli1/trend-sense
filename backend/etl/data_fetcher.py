"""Helper functions to fetch data from external APIs and return structured data."""
import os
import requests
import time
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai
# DÜZELTME 1: "backend." ibaresini kaldırdık çünkü zaten backend klasöründeyiz
from config import Config

# Configure Gemini API
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    # DÜZELTME 2: Model ismini güncel (ve çalışan) versiyonla değiştirdik
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None
    print("Warning: GEMINI_API_KEY not found. Sentiment analysis will return 0.0")


def analyze_sentiment(text: str) -> float:
    """Analyze sentiment of text using Google Gemini API.
    
    Args:
        text: Text to analyze (headline or content)
        
    Returns:
        Sentiment score between -1.0 (negative) and 1.0 (positive).
        Returns 0.0 (neutral) if API fails or key is missing.
    """
    if not gemini_model:
        return 0.0
    
    if not text or not text.strip():
        return 0.0
    
    # Create prompt for sentiment analysis
    prompt = f"""Analyze the sentiment of this tech news headline: '{text}'. Return ONLY a float number between -1.0 (negative) and 1.0 (positive). No explanation."""
    
    # Try with retry logic for 429 errors
    for attempt in range(2):  # Try twice (initial + one retry)
        try:
            # Generate response
            response = gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract float from response (handle cases where Gemini returns text with number)
            # Look for a float pattern in the response
            float_pattern = r'-?\d+\.?\d*'
            matches = re.findall(float_pattern, response_text)
            
            if matches:
                # Get the first number that looks like a float
                sentiment = float(matches[0])
                # Clamp to valid range [-1.0, 1.0]
                sentiment = max(-1.0, min(1.0, sentiment))
                return round(sentiment, 2)
            else:
                # If no number found, return neutral
                print(f"Warning: Could not parse sentiment from response: {response_text}")
                return 0.0
        
        except Exception as e:
            error_str = str(e)
            # Check if it's a 429 Quota Exceeded error
            if '429' in error_str or 'Quota Exceeded' in error_str or 'quota' in error_str.lower():
                if attempt == 0:
                    # First attempt failed with 429, wait and retry
                    print("⚠️ Quota hit. Waiting 20s...")
                    time.sleep(20)
                    continue  # Retry once
                else:
                    # Already retried, give up
                    print(f"   ❌ Rate limit still exceeded after retry. Returning neutral sentiment.")
                    return 0.0
            else:
                # Other error, don't retry
                print(f"Error analyzing sentiment: {e}")
                return 0.0
    
    # If we get here, both attempts failed
    return 0.0


def fetch_hacker_news_data(keyword: str, limit: int = 3) -> List[Dict[str, Any]]:
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
                title = item.get('title', '')
                content = item.get('story_text', '') or title
                
                # Use title for sentiment analysis (more concise)
                text_for_analysis = title if title else content[:200]
                
                # Analyze sentiment using Gemini AI
                sentiment = analyze_sentiment(text_for_analysis)
                
                # Rate limiting: wait 4 seconds after each API call (15 req/min = 4s delay)
                print(f"   (Sleeping for 4s to respect API limits...)")
                time.sleep(4)
                
                results.append({
                    'title': title,
                    'content': content,
                    'url': item.get('url', f"https://news.ycombinator.com/item?id={item.get('objectID', '')}"),
                    'source': 'hackernews',
                    'keyword': keyword,
                    'sentiment': sentiment,
                    'created_at': datetime.fromtimestamp(item.get('created_at_i', 0)).isoformat() if item.get('created_at_i') else datetime.now().isoformat()
                })
    except Exception as e:
        print(f"Error fetching Hacker News data: {e}")
    
    return results


def fetch_news_api_data(keyword: str, limit: int = 3) -> List[Dict[str, Any]]:
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
                    title = item.get('title', '')
                    content = item.get('content', '') or item.get('description', '')
                    
                    # Use title for sentiment analysis (more concise)
                    text_for_analysis = title if title else content[:200]
                    
                    # Analyze sentiment using Gemini AI
                    sentiment = analyze_sentiment(text_for_analysis)
                    
                    # Rate limiting: wait 4 seconds after each API call (15 req/min = 4s delay)
                    print(f"   (Sleeping for 4s to respect API limits...)")
                    time.sleep(4)
                    
                    results.append({
                        'title': title,
                        'content': content,
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
    
    print(f"Fetching trends data for keywords: {', '.join(keywords)}")
    print("Using Google Gemini AI for sentiment analysis...")
    
    for keyword in keywords:
        print(f"\nProcessing keyword: {keyword}")
        
        # Fetch from Hacker News
        print(f"  Fetching from Hacker News...")
        hn_data = fetch_hacker_news_data(keyword, limit=5)
        all_data.extend(hn_data)
        print(f"  Found {len(hn_data)} articles from Hacker News")
        
        # Fetch from News API
        print(f"  Fetching from News API...")
        news_data = fetch_news_api_data(keyword, limit=5)
        all_data.extend(news_data)
        print(f"  Found {len(news_data)} articles from News API")
        
        # Small delay between keywords
        time.sleep(0.5)
    
    print(f"\nTotal articles fetched: {len(all_data)}")
    return all_data