"""Tests for Flask API endpoints."""
import unittest
from backend.app import app


class TestAPI(unittest.TestCase):
    """Test API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
    
    def test_get_keywords(self):
        """Test keywords endpoint."""
        response = self.app.get("/api/keywords")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("keywords", data)
    
    def test_get_sentiments(self):
        """Test sentiments endpoint."""
        response = self.app.get("/api/sentiments")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("count", data)
    
    def test_get_sentiments_with_filters(self):
        """Test sentiments endpoint with filters."""
        response = self.app.get("/api/sentiments?keyword=Python&source=reddit")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
    
    def test_get_stats(self):
        """Test stats endpoint."""
        response = self.app.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("stats", data)
        self.assertIn("total_count", data["stats"])
        self.assertIn("average_sentiment", data["stats"])


if __name__ == "__main__":
    unittest.main()

