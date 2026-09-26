import sys
import os
import unittest
from unittest.mock import patch
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

    def test_01_health_check_success(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertEqual(data["database_name"], "nie_servicehub")

    @patch("app.routes.health.get_database")
    def test_02_health_check_database_failure(self, mock_get_db):
        mock_get_db.side_effect = Exception("Database connection lost")
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["database"].startswith("error:"))

    def test_03_create_request_success(self):
        payload = {
            "title": "ID Card Not Working",
            "description": "Student ID card is not being detected at the library entrance",
            "category": "ID_CARD",
            "priority": "HIGH",
            "created_by": "student01"
        }
        response = self.client.post("/api/requests", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data["request_id"].startswith("REQ-"))
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["category"], "ID_CARD")
        self.assertEqual(data["priority"], "HIGH")
        self.assertEqual(data["status"], "NEW")
        self.assertEqual(data["department"], "Student Services")
        self.__class__.created_request_ids.append(data["request_id"])
        self.__class__.test_req_id = data["request_id"]

    def test_04_get_requests_list(self):
        response = self.client.get("/api/requests")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_05_get_single_request_success(self):
        req_id = self.__class__.test_req_id
        response = self.client.get(f"/api/requests/{req_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["request_id"], req_id)

    def test_06_filter_requests_by_category_and_status(self):
        response = self.client.get("/api/requests?category=ID_CARD&status=NEW")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(all(item["category"] == "ID_CARD" for item in data))

    def test_07_search_requests(self):
        response = self.client.get("/api/requests?search=library")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_08_update_request_info(self):
        req_id = self.__class__.test_req_id
        update_payload = {
            "title": "ID Card Barcode Damaged - Immediate Replacement Required",
            "priority": "URGENT"
        }
        response = self.client.put(f"/api/requests/{req_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], update_payload["title"])
        self.assertEqual(data["priority"], "URGENT")

    def test_09_assign_request(self):
        req_id = self.__class__.test_req_id
        assign_payload = {
            "assigned_to": "Staff Officer Suresh",
            "department": "Student Services Desk"
        }
        response = self.client.patch(f"/api/requests/{req_id}/assign", json=assign_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["assigned_to"], "Staff Officer Suresh")
        # Auto-transitions status from NEW to ASSIGNED
        self.assertEqual(data["status"], "ASSIGNED")

    def test_10_valid_status_transitions(self):
        req_id = self.__class__.test_req_id
        # ASSIGNED -> IN_PROGRESS
        res1 = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "IN_PROGRESS"})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.json()["status"], "IN_PROGRESS")

        # IN_PROGRESS -> RESOLVED
        res2 = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "RESOLVED"})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()["status"], "RESOLVED")

        # RESOLVED -> CLOSED
        res3 = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "CLOSED"})
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res3.json()["status"], "CLOSED")

    def test_11_invalid_status_transition_fails(self):
        req_id = self.__class__.test_req_id
        # Current status is CLOSED -> Invalid transition to ON_HOLD
        response = self.client.patch(f"/api/requests/{req_id}/status", json={"status": "ON_HOLD"})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("Invalid status transition", data["detail"])

    def test_12_nonexistent_request_returns_404(self):
        response = self.client.get("/api/requests/REQ-999999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("not found", data["detail"])

    def test_13_validation_failure_empty_title_returns_422(self):
        invalid_payload = {
            "title": "   ",
            "description": "Short",
            "category": "INVALID_CATEGORY"
        }
        response = self.client.post("/api/requests", json=invalid_payload)
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data["error"], "Validation Error")

    def test_14_delete_request_success(self):
        payload = {
            "title": "Temp Request for Delete Test",
            "description": "Will be deleted automatically.",
            "category": "HOSTEL"
        }
        create_res = self.client.post("/api/requests", json=payload)
        req_id = create_res.json()["request_id"]

        del_res = self.client.delete(f"/api/requests/{req_id}")
        self.assertEqual(del_res.status_code, 204)

        get_res = self.client.get(f"/api/requests/{req_id}")
        self.assertEqual(get_res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
