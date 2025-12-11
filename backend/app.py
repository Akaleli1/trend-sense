"""Flask API server for Tech Trend Sentiment Analyst."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from typing import Optional
from config import Config
from database.db import Database
from etl.data_fetcher import fetch_all_trends_data

app = Flask(__name__)
# Enable CORS for frontend (allow requests from localhost:3000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

db = Database()


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/api/sentiments", methods=["GET"])
def get_sentiments():
    """Get sentiment data with optional filters.
    
    Query parameters:
        keyword: Filter by keyword
        source: Filter by source (reddit, news)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Maximum number of results
    """
    try:
        keyword = request.args.get("keyword")
        source = request.args.get("source")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        limit = request.args.get("limit", type=int)
        
        # Default to last 30 days if no dates provided
        if not start_date and not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        sentiments = db.get_sentiments(
            keyword=keyword,
            source=source,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "count": len(sentiments),
            "data": sentiments
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/keywords", methods=["GET"])
def get_keywords():
    """Get all available keywords."""
    try:
        keywords = db.get_keywords()
        return jsonify({
            "success": True,
            "keywords": keywords
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get statistics for sentiments.
    
    Query parameters:
        keyword: Filter by keyword (optional)
    """
    try:
        keyword = request.args.get("keyword")
        stats = db.get_stats(keyword=keyword)
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.route("/api/trends", methods=["GET"])
def get_trends():
    """Get trend data from external APIs (Hacker News and News API).
    
    This endpoint fetches real data from external sources and returns
    sentiment scores.
    
    Query parameters:
        keywords: Comma-separated list of keywords (optional, defaults to config)
    """
    try:
        # Get keywords from query params or use default
        keywords_param = request.args.get("keywords")
        keywords = None
        if keywords_param:
            keywords = [k.strip() for k in keywords_param.split(",")]
        
        # Fetch data from external APIs
        trends_data = fetch_all_trends_data(keywords)
        
        # Transform data for chart consumption
        # Group by keyword and date, calculate average sentiment per day
        chart_data = {}
        
        for item in trends_data:
            # DÜZELTME 1: Keyword'ün boş gelme ihtimaline karşı sıkı kontrol
            keyword = item.get('keyword')
            if not keyword:
                keyword = 'Unknown'
                
            # Date handling
            raw_date = item.get('created_at', datetime.now().isoformat())
            try:
                date = raw_date.split('T')[0]
            except:
                date = datetime.now().strftime("%Y-%m-%d")

            sentiment = item.get('sentiment', 0.0)
            
            # Benzersiz anahtar oluştur
            key = f"{keyword}_{date}"
            
            if key not in chart_data:
                chart_data[key] = {
                    'keyword': keyword,
                    'date': date,
                    'sentiments': [],
                    'articles': 0
                }
            
            chart_data[key]['sentiments'].append(sentiment)
            chart_data[key]['articles'] += 1
        
        # Calculate averages and format for chart
        formatted_data = []
        for key, data in chart_data.items():
            avg_sentiment = sum(data['sentiments']) / len(data['sentiments']) if data['sentiments'] else 0.0
            
            formatted_data.append({
                'date': data['date'],
                'keyword': data['keyword'],
                # DÜZELTME 2: Recharts için 'name' alanı eklendi (Tooltip bunu sever)
                'name': data['keyword'], 
                'sentiment': round(avg_sentiment, 2),
                'articles': data['articles']
            })
        
        # Sort by date
        formatted_data.sort(key=lambda x: x['date'])
        
        return jsonify({
            "success": True,
            "count": len(formatted_data),
            "data": formatted_data,
            # Debug için raw_data'yı da gönderiyoruz
            "raw_data": trends_data[:5] 
        })
    
    except Exception as e:
        print(f"Error in get_trends: {e}") # Backend terminalinde hatayı görmek için
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )

