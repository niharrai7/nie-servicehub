from typing import List, Optional
from fastapi import APIRouter, Query, status
from app.models.service_request import Status, Category, Priority
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestUpdate,
    ServiceRequestStatusUpdate,
    ServiceRequestAssign,
    ServiceRequestResponse
)
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["Service Requests"])

@router.post(
    "",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Service Request",
    description="Raise a new service request for student/faculty services (ID Card, Bonafide, Hostel, Transport, Library, IT Support)."
)
def create_service_request(payload: ServiceRequestCreate):
    created_doc = RequestService.create_request(payload)
    return ServiceRequestResponse.model_validate(created_doc)

@router.get(
    "",
    response_model=List[ServiceRequestResponse],
    status_code=status.HTTP_200_OK,
    summary="List Service Requests",
    description="Retrieve service requests with optional filters for status, category, priority, or search term."
)
def list_service_requests(
    status_filter: Optional[Status] = Query(None, alias="status", description="Filter by status (NEW, ASSIGNED, IN_PROGRESS, ON_HOLD, RESOLVED, CLOSED)"),
    category_filter: Optional[Category] = Query(None, alias="category", description="Filter by category"),
    priority_filter: Optional[Priority] = Query(None, alias="priority", description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search keyword in title, description, request_id, or creator")
):
    requests = RequestService.get_requests(
        status_filter=status_filter,
        category_filter=category_filter,
        priority_filter=priority_filter,
        search=search
    )
    return [ServiceRequestResponse.model_validate(r) for r in requests]

@router.get(
    "/{request_id}",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Service Request Details",
    description="Retrieve details of a single service request by its unique request ID (e.g. REQ-1001)."
)
def get_service_request(request_id: str):
    doc = RequestService.get_request_by_id(request_id)
    return ServiceRequestResponse.model_validate(doc)

@router.put(
    "/{request_id}",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Service Request Details",
    description="Update non-lifecycle fields (title, description, category, priority) of a service request."
)
def update_service_request(request_id: str, payload: ServiceRequestUpdate):
    updated_doc = RequestService.update_request(request_id, payload)
    return ServiceRequestResponse.model_validate(updated_doc)

@router.patch(
    "/{request_id}/status",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Request Lifecycle Status",
    description="Advance or change the status of a service request following the request lifecycle rules."
)
def update_request_status(request_id: str, payload: ServiceRequestStatusUpdate):
    updated_doc = RequestService.update_status(request_id, payload.status)
    return ServiceRequestResponse.model_validate(updated_doc)

@router.patch(
    "/{request_id}/assign",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_200_OK,
    summary="Assign Staff / Department",
    description="Assign a staff member and department to handle the service request. Automatically sets status to ASSIGNED if currently NEW."
)
def assign_service_request(request_id: str, payload: ServiceRequestAssign):
    updated_doc = RequestService.assign_request(request_id, payload)
    return ServiceRequestResponse.model_validate(updated_doc)

@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Service Request",
    description="Permanently delete a service request from the system."
)
def delete_service_request(request_id: str):
    RequestService.delete_request(request_id)
    return None
