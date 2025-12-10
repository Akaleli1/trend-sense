"""AI transformation using Google Gemini API."""
import json
import time
from typing import Dict, Any, Optional
import google.generativeai as genai
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.config import Config


class SentimentTransformer:
    """Transform text data using Gemini API for sentiment analysis."""
    
    def __init__(self):
        """Initialize Gemini API client."""
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def _create_prompt(self, keyword: str, content: str) -> str:
        """Create prompt for sentiment analysis.
        
        Args:
            keyword: Technology keyword
            content: Text content to analyze
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze the following text about {keyword} and provide a sentiment analysis.

Text: {content[:2000]}

Please provide your analysis in JSON format with the following structure:
{{
    "sentiment_score": <float between -1.0 (very negative) and +1.0 (very positive)>,
    "summary": "<2-3 sentence summary of the text and its sentiment>"
}}

Important:
- sentiment_score must be a float between -1.0 and 1.0
- summary should be 2-3 sentences
- Respond ONLY with valid JSON, no additional text"""
        
        return prompt
    
    def analyze_sentiment(self, keyword: str, title: str, content: str) -> Optional[Dict[str, Any]]:
        """Analyze sentiment of text using Gemini API.
        
        Args:
            keyword: Technology keyword
            title: Article/post title
            content: Article/post content
            
        Returns:
            Dictionary with sentiment_score and summary, or None if error
        """
        if not self.model:
            return None
        
        # Combine title and content for analysis
        full_text = f"{title}\n\n{content}"
        
        try:
            prompt = self._create_prompt(keyword, full_text)
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Try to find JSON in the response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate sentiment score
            sentiment_score = float(result.get("sentiment_score", 0.0))
            if sentiment_score < -1.0:
                sentiment_score = -1.0
            elif sentiment_score > 1.0:
                sentiment_score = 1.0
            
            return {
                "sentiment_score": sentiment_score,
                "summary": result.get("summary", "No summary available.")
            }
        
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response_text if 'response_text' in locals() else 'N/A'}")
            return None
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return None
    
    def transform_batch(self, data: list) -> list:
        """Transform a batch of data records.
        
        Args:
            data: List of data dictionaries from extract phase
            
        Returns:
            List of transformed data with sentiment analysis
        """
        transformed = []
        
        for record in data:
            result = self.analyze_sentiment(
                keyword=record.get("keyword", ""),
                title=record.get("title", ""),
                content=record.get("content", "")
            )
            
            if result:
                record.update(result)
                transformed.append(record)
            else:
                print(f"Failed to analyze sentiment for: {record.get('title', 'Unknown')}")
            
            # Rate limiting
            time.sleep(1)
        
        return transformed

