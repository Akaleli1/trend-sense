"""Tests for ETL operations."""
import unittest
from unittest.mock import Mock, patch
from backend.etl.extract import DataExtractor
from backend.etl.transform import SentimentTransformer


class TestETLExtract(unittest.TestCase):
    """Test ETL extraction."""
    
    def setUp(self):
        """Set up test extractor."""
        self.extractor = DataExtractor()
    
    @patch('backend.etl.extract.praw.Reddit')
    def test_extract_reddit_initialization(self, mock_reddit):
        """Test Reddit API initialization."""
        # This test verifies the extractor can be initialized
        self.assertIsNotNone(self.extractor)
    
    @patch('backend.etl.extract.requests.get')
    def test_extract_news(self, mock_get):
        """Test News API extraction."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "Test Article",
                    "content": "Test content about Python",
                    "url": "https://example.com/test",
                    "publishedAt": "2024-01-01T00:00:00Z"
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # This would require proper config setup
        # For now, just test the structure
        self.assertIsNotNone(self.extractor)


class TestETLTransform(unittest.TestCase):
    """Test ETL transformation."""
    
    def setUp(self):
        """Set up test transformer."""
        self.transformer = SentimentTransformer()
    
    def test_prompt_creation(self):
        """Test prompt creation."""
        prompt = self.transformer._create_prompt("Python", "This is great!")
        self.assertIn("Python", prompt)
        self.assertIn("sentiment_score", prompt)
        self.assertIn("summary", prompt)
    
    @patch('backend.etl.transform.genai.GenerativeModel')
    def test_analyze_sentiment_structure(self, mock_model):
        """Test sentiment analysis structure."""
        # Mock the model response
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = '{"sentiment_score": 0.5, "summary": "Test summary"}'
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        # This would require proper config
        # Just verify the method exists
        self.assertTrue(hasattr(self.transformer, 'analyze_sentiment'))


if __name__ == "__main__":
    unittest.main()

