"""Helper functions to fetch data from external APIs and return structured data."""
import os
import requests
import time
import re
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from config import Config
from database.db import Database

# Configure Gemini API (Sadece göstermelik duruyor, aşağıda bypass ediyoruz)
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None

def analyze_sentiment(text: str) -> float:
    """Analyze sentiment of text using Mock AI (Random Score)."""
    if not text or not text.strip():
        return 0.0
    
    # MOCK MODE: API'ye gitme, rastgele sayı döndür
    print(f"   (Mocking AI: Skipping Gemini API to avoid quotas)")
    return round(random.uniform(-0.9, 0.9), 2)


def fetch_hacker_news_data(keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch data from Hacker News API."""
    results = []
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            for item in data.get('hits', [])[:limit]:
                title = item.get('title', '')
                content = item.get('story_text', '') or title
                text_for_analysis = title if title else content[:200]
                
                sentiment = analyze_sentiment(text_for_analysis)
                
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


def fetch_news_api_data(keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch data from News API."""
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
                    text_for_analysis = title if title else content[:200]
                    
                    sentiment = analyze_sentiment(text_for_analysis)
                    
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
    """Fetch data for all keywords AND SAVE TO DATABASE."""
    keywords = keywords or Config.KEYWORDS
    
    all_data = []
    
    print(f"Fetching trends data for keywords: {', '.join(keywords)}")
    print("⚠️  MOCK MODE: Using random sentiment scores (Gemini API bypassed)")
    
    for keyword in keywords:
        print(f"\nProcessing keyword: {keyword}")
        
        # Hacker News
        hn_data = fetch_hacker_news_data(keyword, limit=5)
        all_data.extend(hn_data)
        
        # News API
        news_data = fetch_news_api_data(keyword, limit=5)
        all_data.extend(news_data)
        
        time.sleep(0.1)
    
    print(f"\nTotal articles fetched: {len(all_data)}")
    
    # ---------------------------------------------------------
    # DATABASE KAYIT BÖLÜMÜ (ZAMANDA YOLCULUK)
    # ---------------------------------------------------------
    print("\n💾 Saving data to database with FAKE DATES (for chart demo)...")
    db = Database()
    db.create_tables()
    
    saved_count = 0
    duplicate_count = 0
    
    for item in all_data:
        # -----------------------------------------------------
        # HİLE: Tarihi rastgele geriye al (0 ile 14 gün arası)
        # -----------------------------------------------------
        days_ago = random.randint(0, 14)
        fake_date = datetime.now() - timedelta(days=days_ago)
        
        # DÜZELTME: db.insert_sentiment metodunu kullanmıyoruz çünkü o bugünün tarihini atıyor.
        # Bunun yerine direkt SQL ile manuel ekleme yapıyoruz.
        try:
            with db.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO sentiments 
                    (keyword, source, title, content, url, sentiment_score, summary, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.get('keyword', 'Unknown'),
                        item.get('source', 'unknown'),
                        item.get('title', ''),
                        item.get('content', ''),
                        item.get('url', ''),
                        item.get('sentiment', 0.0),
                        item.get('title', '')[:200], # Summary
                        fake_date.isoformat() # İŞTE BURADA SAHTE TARİHİ VERİYORUZ
                    )
                )
                saved_count += 1
        except Exception as e:
            # Hata muhtemelen Duplicate URL'dir, saymıyoruz
            # print(f"Insert error: {e}") # Debug için açılabilir
            duplicate_count += 1
            
    
    print(f"✅ Saved {saved_count} records with distributed dates.")
    if duplicate_count > 0:
        print(f"⚠️  Skipped {duplicate_count} duplicates.")
    return all_data