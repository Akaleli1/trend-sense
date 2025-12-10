"""Tests for database operations."""
import unittest
import os
import tempfile
from backend.database.db import Database


class TestDatabase(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_insert_sentiment(self):
        """Test inserting a sentiment record."""
        result = self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test Post",
            content="This is a test post about Python.",
            url="https://example.com/test",
            sentiment_score=0.5,
            summary="Test summary"
        )
        self.assertTrue(result)
    
    def test_insert_duplicate(self):
        """Test inserting duplicate URL."""
        self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test Post",
            content="This is a test post.",
            url="https://example.com/test",
            sentiment_score=0.5,
            summary="Test summary"
        )
        # Try to insert again with same URL
        result = self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test Post 2",
            content="Different content",
            url="https://example.com/test",
            sentiment_score=0.6,
            summary="Different summary"
        )
        self.assertFalse(result)  # Should fail due to duplicate
    
    def test_get_sentiments(self):
        """Test retrieving sentiments."""
        # Insert test data
        self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test Post",
            content="Test content",
            url="https://example.com/test1",
            sentiment_score=0.5,
            summary="Test summary"
        )
        
        sentiments = self.db.get_sentiments(keyword="Python")
        self.assertEqual(len(sentiments), 1)
        self.assertEqual(sentiments[0]["keyword"], "Python")
    
    def test_get_keywords(self):
        """Test retrieving keywords."""
        self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test",
            content="Test",
            url="https://example.com/test1",
            sentiment_score=0.5,
            summary="Test"
        )
        self.db.insert_sentiment(
            keyword="JavaScript",
            source="news",
            title="Test",
            content="Test",
            url="https://example.com/test2",
            sentiment_score=0.3,
            summary="Test"
        )
        
        keywords = self.db.get_keywords()
        self.assertIn("Python", keywords)
        self.assertIn("JavaScript", keywords)
    
    def test_get_stats(self):
        """Test retrieving statistics."""
        self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test",
            content="Test",
            url="https://example.com/test1",
            sentiment_score=0.5,
            summary="Test"
        )
        self.db.insert_sentiment(
            keyword="Python",
            source="reddit",
            title="Test 2",
            content="Test",
            url="https://example.com/test2",
            sentiment_score=0.7,
            summary="Test"
        )
        
        stats = self.db.get_stats(keyword="Python")
        self.assertEqual(stats["total_count"], 2)
        self.assertAlmostEqual(stats["average_sentiment"], 0.6, places=1)


if __name__ == "__main__":
    unittest.main()

