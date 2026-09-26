import sys
import os
import unittest
from fastapi.testclient import TestClient

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

class TestServiceRequestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.created_request_ids = []

    @classmethod
    def tearDownClass(cls):
        # Clean up created test requests from MongoDB database
        for req_id in cls.created_request_ids:
            cls.client.delete(f"/api/requests/{req_id}")
        from app.database import close_database
        close_database()

    def test_01_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")

    def test_02_create_request(self):
        payload = {
            "title": "Library Book Renewal Issue",
            "description": "Unable to renew book ID B-402 online via library portal.",
            "category": "LIBRARY",
            "priority": "HIGH",
            "created_by": "Faculty Dr. Ananya"
        }
        response = self.client.post("/api/requests", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data["request_id"].startswith("REQ-"))
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["category"], "LIBRARY")
        self.assertEqual(data["status"], "NEW")
        self.__class__.created_request_ids.append(data["request_id"])
        self.__class__.test_req_id = data["request_id"]

    def test_03_get_requests(self):
        response = self.client.get("/api/requests")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_04_get_single_request(self):
        req_id = self.__class__.test_req_id
        response = self.client.get(f"/api/requests/{req_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["request_id"], req_id)

    def test_05_filter_requests(self):
        response = self.client.get("/api/requests?category=LIBRARY&status=NEW")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(all(item["category"] == "LIBRARY" for item in data))

    def test_06_update_request(self):
        req_id = self.__class__.test_req_id
        update_payload = {
            "title": "Library Book Renewal Issue - URGENT",
            "priority": "URGENT"
        }
        response = self.client.put(f"/api/requests/{req_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], update_payload["title"])
        self.assertEqual(data["priority"], "URGENT")

    def test_07_assign_request(self):
        req_id = self.__class__.test_req_id
        assign_payload = {
            "assigned_to": "Librarian Ramesh",
            "department": "Library Services"
        }
        response = self.client.patch(f"/api/requests/{req_id}/assign", json=assign_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["assigned_to"], "Librarian Ramesh")
        # Automatic transition from NEW to ASSIGNED
        self.assertEqual(data["status"], "ASSIGNED")

    def test_08_valid_status_transition(self):
        req_id = self.__class__.test_req_id
        # Current status is ASSIGNED -> Allowed transition to IN_PROGRESS
        response = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "IN_PROGRESS"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "IN_PROGRESS")

    def test_09_invalid_status_transition(self):
        req_id = self.__class__.test_req_id
        # Current status is IN_PROGRESS -> Invalid transition to NEW (must fail with HTTP 400)
        response = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "NEW"})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("Invalid status transition", data["detail"])

    def test_10_nonexistent_request(self):
        response = self.client.get("/api/requests/REQ-999999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("not found", data["detail"])

    def test_11_validation_failure(self):
        invalid_payload = {
            "title": "AB", # Title too short (min 3 chars)
            "description": "Short",
            "category": "INVALID_CATEGORY"
        }
        response = self.client.post("/api/requests", json=invalid_payload)
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data["error"], "Validation Error")

    def test_12_delete_request(self):
        # Create temporary request to delete
        payload = {
            "title": "Temporary Request to Delete",
            "description": "Will be deleted shortly in test execution.",
            "category": "TRANSPORT"
        }
        create_res = self.client.post("/api/requests", json=payload)
        req_id = create_res.json()["request_id"]

        del_res = self.client.delete(f"/api/requests/{req_id}")
        self.assertEqual(del_res.status_code, 204)

        # Confirm deleted
        get_res = self.client.get(f"/api/requests/{req_id}")
        self.assertEqual(get_res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
