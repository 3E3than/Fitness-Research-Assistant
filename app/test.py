import requests
import json
from typing import Dict, Any
from datetime import datetime

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def test_and_print(self, name: str, response: requests.Response) -> None:
        """Print formatted test results"""
        print(f"\n=== {name} ===")
        print(f"Status Code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)

    def run_all_tests(self):
        """Run all API tests"""
        # Test article creation
        article_data = {
            "url": "https://example.com/test2",
            "title": "Test Article1",
            "content": "Test content",
            "summary": "Test summary",
            "source": "example.com",
            "tags": ["test", "api"]
        }
        response = self.session.post(f"{self.base_url}/articles/", json=article_data)
        self.test_and_print("Create Article", response)
        
        # Store article ID for later tests
        article_id = response.json()["id"]

        # Test article retrieval
        response = self.session.get(f"{self.base_url}/articles/{article_id}")
        self.test_and_print("Get Article", response)

        # Test search
        search_data = {
            "query": "test",
            "page": 1,
            "per_page": 10
        }
        response = self.session.post(f"{self.base_url}/search/", json=search_data)
        self.test_and_print("Search Articles", response)

        # Test update
        update_data = article_data.copy()
        update_data["title"] = "Updated Test Article"
        response = self.session.put(f"{self.base_url}/articles/{article_id}", 
                                  json=update_data)
        self.test_and_print("Update Article", response)

        # Test delete
        response = self.session.delete(f"{self.base_url}/articles/{article_id}")
        self.test_and_print("Delete Article", response)

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()