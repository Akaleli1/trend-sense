import os
import requests
from dotenv import load_dotenv

# 1. Load environment variables (API Keys)
load_dotenv() 

# ---------------------------------------------------------
# Source 1: Hacker News (No Key Needed)
# ---------------------------------------------------------
def fetch_hacker_news(keyword):
    print(f"\n🔎 Fetching Hacker News data for: {keyword}...")
    
    url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Print first 3 results
        for item in data['hits'][:3]:
            print(f"   [HN] {item['title']}")
    else:
        print(f"   ❌ Error fetching Hacker News: {response.status_code}")

# ---------------------------------------------------------
# Source 2: News API (Requires Key from .env)
# ---------------------------------------------------------
def fetch_news_api(keyword):
    print(f"\n📰 Fetching News API data for: {keyword}...")
    
    # Get the key securely from .env
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        print("   ❌ Error: NEWS_API_KEY not found. Please check your .env file.")
        return

    # News API Endpoint
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': keyword,
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 3  # Limit to 3 for testing
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['totalResults'] > 0:
            for item in data['articles']:
                print(f"   [News] {item['title']}")
        else:
            print("   No news found.")
    else:
        print(f"   ❌ Error fetching News API: {response.status_code} - {response.text}")

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    # Test with specific keywords
    keywords = ["Next.js", "Python", "Artificial Intelligence"]
    
    for kw in keywords:
        fetch_hacker_news(kw)
        fetch_news_api(kw)
        print("-" * 50)