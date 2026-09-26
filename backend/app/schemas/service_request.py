from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from app.models.service_request import Category, Priority, Status

class ServiceRequestCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Brief summary of the request", example="ID Card not working at library")
    description: str = Field(..., min_length=5, max_length=1000, description="Detailed explanation of the request", example="My student ID card fails to scan at the central library gate.")
    category: Category = Field(..., description="Service request category", example=Category.ID_CARD)
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level", example=Priority.MEDIUM)
    created_by: str = Field(default="Student", min_length=2, max_length=50, description="Creator name or ID", example="Student John Doe")
    department: Optional[str] = Field(default=None, max_length=100, description="Department handling the request", example="Student Services")

    @field_validator("title", "description", "created_by", mode="before")
    @classmethod
    def check_not_empty_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise ValueError("Field cannot be empty or contain only whitespace.")
            return stripped
        return value

class ServiceRequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=1000)
    category: Optional[Category] = None
    priority: Optional[Priority] = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def check_not_empty_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise ValueError("Field cannot be empty or contain only whitespace.")
            return stripped
        return value

class ServiceRequestStatusUpdate(BaseModel):
    status: Status = Field(..., description="New status for the service request", example=Status.ASSIGNED)

class ServiceRequestAssign(BaseModel):
    assigned_to: str = Field(..., min_length=2, max_length=50, description="Staff member assigned to request", example="Staff Member Jane")
    department: Optional[str] = Field(None, max_length=100, description="Target department", example="IT Helpdesk")

    @field_validator("assigned_to", "department", mode="before")
    @classmethod
    def check_not_empty_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise ValueError("Field cannot be empty or contain only whitespace.")
            return stripped
        return value

class ServiceRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: str
    title: str
    description: str
    category: Category
    priority: Priority
    status: Status
    created_by: str
    assigned_to: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime
    updated_at: datetime
