from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.database import get_database
from app.models.service_request import Status, Category, Priority, VALID_TRANSITIONS
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestUpdate,
    ServiceRequestAssign,
    ServiceRequestResponse
)

# Department Mapping Defaults by Category
DEFAULT_DEPARTMENTS: Dict[Category, str] = {
    Category.BONAFIDE: "Academic Affairs",
    Category.ID_CARD: "Student Services",
    Category.HOSTEL: "Hostel Management",
    Category.TRANSPORT: "Transport Department",
    Category.LIBRARY: "Library Services",
    Category.IT_SUPPORT: "IT Helpdesk"
}

def get_collection():
    db = get_database()
    return db["service_requests"]

def get_counters_collection():
    db = get_database()
    return db["counters"]

def generate_request_id() -> str:
    """Generate sequential human-readable request IDs like REQ-1001, REQ-1002"""
    counters = get_counters_collection()
    counter = counters.find_one_and_update(
        {"_id": "request_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    # Start sequence at 1001
    seq = counter.get("seq", 1) + 1000
    return f"REQ-{seq}"

class RequestService:

    @staticmethod
    def create_request(data: ServiceRequestCreate) -> Dict[str, Any]:
        col = get_collection()
        now = datetime.now(timezone.utc)
        
        req_id = generate_request_id()
        dept = data.department or DEFAULT_DEPARTMENTS.get(data.category, "General Support")

        document = {
            "request_id": req_id,
            "title": data.title.strip(),
            "description": data.description.strip(),
            "category": data.category.value,
            "priority": data.priority.value,
            "status": Status.NEW.value,
            "created_by": data.created_by.strip(),
            "assigned_to": None,
            "department": dept,
            "created_at": now,
            "updated_at": now
        }

        col.insert_one(document)
        return document

    @staticmethod
    def get_requests(
        status_filter: Optional[Status] = None,
        category_filter: Optional[Category] = None,
        priority_filter: Optional[Priority] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        col = get_collection()
        query: Dict[str, Any] = {}

        if status_filter:
            query["status"] = status_filter.value
        if category_filter:
            query["category"] = category_filter.value
        if priority_filter:
            query["priority"] = priority_filter.value
        if search:
            regex_pattern = {"$regex": search.strip(), "$options": "i"}
            query["$or"] = [
                {"title": regex_pattern},
                {"description": regex_pattern},
                {"request_id": regex_pattern},
                {"created_by": regex_pattern}
            ]

        cursor = col.find(query).sort("created_at", -1)
        return list(cursor)

    @staticmethod
    def get_request_by_id(request_id: str) -> Dict[str, Any]:
        col = get_collection()
        doc = col.find_one({"request_id": request_id})
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service request with ID '{request_id}' not found."
            )
        return doc

    @staticmethod
    def update_request(request_id: str, data: ServiceRequestUpdate) -> Dict[str, Any]:
        col = get_collection()
        existing = RequestService.get_request_by_id(request_id)

        update_fields: Dict[str, Any] = {}
        if data.title is not None:
            update_fields["title"] = data.title.strip()
        if data.description is not None:
            update_fields["description"] = data.description.strip()
        if data.category is not None:
            update_fields["category"] = data.category.value
        if data.priority is not None:
            update_fields["priority"] = data.priority.value

        if not update_fields:
            return existing

        update_fields["updated_at"] = datetime.now(timezone.utc)
        col.update_one({"request_id": request_id}, {"$set": update_fields})
        return RequestService.get_request_by_id(request_id)

    @staticmethod
    def update_status(request_id: str, new_status: Status) -> Dict[str, Any]:
        col = get_collection()
        existing = RequestService.get_request_by_id(request_id)
        current_status = Status(existing["status"])

        if new_status == current_status:
            return existing

        # Validate Lifecycle Transition
        allowed_next = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed_next:
            allowed_names = [s.value for s in allowed_next]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from '{current_status.value}' to '{new_status.value}'. "
                       f"Allowed next status transitions: {allowed_names}"
            )

        now = datetime.now(timezone.utc)
        col.update_one(
            {"request_id": request_id},
            {"$set": {"status": new_status.value, "updated_at": now}}
        )
        return RequestService.get_request_by_id(request_id)

    @staticmethod
    def assign_request(request_id: str, data: ServiceRequestAssign) -> Dict[str, Any]:
        col = get_collection()
        existing = RequestService.get_request_by_id(request_id)

        now = datetime.now(timezone.utc)
        update_fields: Dict[str, Any] = {
            "assigned_to": data.assigned_to.strip(),
            "updated_at": now
        }
        if data.department:
            update_fields["department"] = data.department.strip()

        # If ticket was NEW, automatically update status to ASSIGNED
        if existing["status"] == Status.NEW.value:
            update_fields["status"] = Status.ASSIGNED.value

        col.update_one({"request_id": request_id}, {"$set": update_fields})
        return RequestService.get_request_by_id(request_id)

    @staticmethod
    def delete_request(request_id: str) -> None:
        col = get_collection()
        existing = RequestService.get_request_by_id(request_id)
        col.delete_one({"request_id": request_id})
