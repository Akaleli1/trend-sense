"""Helper functions to fetch REAL data and analyze with Gemini AI."""
import os
import requests
import time
import re
import random
from typing import List, Dict, Any
from datetime import datetime
import google.generativeai as genai
from config import Config
from database.db import Database

# --- GEMINI AYARLARI ---
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None
    print("Warning: GEMINI_API_KEY bulunamadı!")

def analyze_sentiment(text: str) -> float:
    """REAL Gemini AI Analysis."""
    if not text or not text.strip(): return 0.0
    if not gemini_model: return 0.0

    # Prompt
    prompt = f"""Analyze the sentiment of this tech news headline: '{text}'. 
    Return ONLY a float number between -1.0 (negative) and 1.0 (positive). No explanation."""
    
    # Retry Logic (429 Hataları için)
    for attempt in range(3): # Deneme sayısını 3'e çıkardık
        try:
            response = gemini_model.generate_content(prompt)
            # Sayıyı ayıkla (regex ile)
            match = re.search(r'-?\d+\.?\d*', response.text)
            if match:
                score = float(match.group())
                return max(-1.0, min(1.0, score)) # Sınırla
            return 0.0
        except Exception as e:
            if "429" in str(e) or "Quota" in str(e) or "429" in str(e):
                wait_time = 60 # 60 Saniye bekle (Google Free Tier çok hassas)
                print(f"⚠️  Kota Sınırı (429). {wait_time} saniye bekleniyor... (Deneme {attempt+1}/3)")
                time.sleep(wait_time)
            else:
                print(f"AI Hatası: {e}")
                return 0.0
    
    print("   ❌ Analiz başarısız (Varsayılan 0.0 atandı)")
    return 0.0

def fetch_all_trends_data(keywords: List[str] = None) -> List[Dict[str, Any]]:
    """Fetch real data, check DB cache, analyze new ones."""
    keywords = keywords or Config.KEYWORDS
    
    db = Database()
    db.create_tables()
    
    # İşlenen tüm verileri toplamak için liste
    total_processed = []
    
    print(f"🔍 Trendler taranıyor: {', '.join(keywords)}")

    for keyword in keywords:
        print(f"\n--- İşleniyor: {keyword} ---")
        
        # 1. Kaynaklardan Veriyi Çek
        raw_articles = []
        
        # Hacker News
        try:
            # timeout süresini artırdık
            hn_resp = requests.get(f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story", timeout=10).json()
            for item in hn_resp.get('hits', [])[:3]: 
                raw_articles.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', f"https://news.ycombinator.com/item?id={item.get('objectID')}"),
                    'source': 'hackernews',
                    'keyword': keyword
                })
        except Exception as e: print(f"HN Hatası: {e}")

        # News API
        api_key = os.getenv("NEWS_API_KEY")
        if api_key:
            try:
                news_resp = requests.get("https://newsapi.org/v2/everything", params={'q': keyword, 'apiKey': api_key, 'pageSize': 3, 'language': 'en'}, timeout=10).json()
                for item in news_resp.get('articles', [])[:3]:
                    raw_articles.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'source': 'news',
                        'keyword': keyword
                    })
            except Exception as e: print(f"NewsAPI Hatası: {e}")

        # 2. Veritabanı Kontrolü ve Analiz
        new_count = 0
        for article in raw_articles:
            # EĞER URL ZATEN VARSA -> ATLAMA
            if db.check_if_url_exists(article['url']):
                print(f"   ⏭️  Atlandı: {article['title'][:30]}...")
                continue
            
            # YOKSA -> GEMINI'YE SOR
            print(f"   🧠 AI Analiz Ediyor: {article['title'][:40]}...")
            sentiment = analyze_sentiment(article['title'])
            
            # Kaydet
            success = db.insert_sentiment(
                keyword=article['keyword'],
                source=article['source'],
                title=article['title'],
                content='',
                url=article['url'],
                sentiment_score=sentiment,
                summary=article['title']
            )
            
            if success:
                new_count += 1
                total_processed.append(article)
            
            # 🔥 HIZ FRENI: Her başarılı API isteğinden sonra 10 saniye bekle
            # Bu, "Requests Per Minute" (RPM) limitini aşmamızı engeller.
            print("   ⏳ API soğutma (10sn)...")
            time.sleep(10) 
            
        print(f"   ✅ {new_count} yeni makale kaydedildi.")

    # init_db.py'nin hata vermemesi için dolu liste döndür
    # Eğer hiç yeni veri yoksa bile, işlem yapıldığını belirtmek için True gibi davranacak bir liste dönüyoruz.
    if not total_processed:
        return [{"status": "completed_no_new_data"}]
        
    return total_processed