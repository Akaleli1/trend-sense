"""Flask API server for Tech Trend Sentiment Analyst."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from typing import Optional
from backend.config import Config
from backend.database.db import Database

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

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

