import sys
import os
from datetime import datetime, timezone

# Ensure app package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_database, close_database

def test_mongodb_connection():
    print("=== NIE ServiceHub: Testing MongoDB Connection ===")
    try:
        db = get_database()
        print(f"[PASS] Successfully connected to database: {db.name}")

        # Test insert document into 'test_collection'
        test_col = db["connection_test"]
        test_doc = {
            "test_key": "day1_test",
            "message": "NIE ServiceHub database connection established successfully!",
            "timestamp": datetime.now(timezone.utc)
        }

        result = test_col.insert_one(test_doc)
        print(f"[PASS] Inserted test document ID: {result.inserted_id}")

        # Test query document
        fetched = test_col.find_one({"_id": result.inserted_id})
        print(f"[PASS] Retrieved document message: '{fetched['message']}'")

        # Cleanup test document
        test_col.delete_one({"_id": result.inserted_id})
        print("[PASS] Cleaned up test document from database.")

        close_database()
        print("=== Database Connection Test Completed Successfully ===")
        return True
    except Exception as e:
        print(f"[FAIL] MongoDB connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
