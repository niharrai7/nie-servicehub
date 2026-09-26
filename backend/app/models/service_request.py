from enum import Enum
from datetime import datetime, timezone
from typing import Optional, Dict, Any

class Category(str, Enum):
    BONAFIDE = "BONAFIDE"
    ID_CARD = "ID_CARD"
    HOSTEL = "HOSTEL"
    TRANSPORT = "TRANSPORT"
    LIBRARY = "LIBRARY"
    IT_SUPPORT = "IT_SUPPORT"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class Status(str, Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

# Allowed Status Transitions Map
VALID_TRANSITIONS: Dict[Status, list[Status]] = {
    Status.NEW: [Status.ASSIGNED, Status.CLOSED],
    Status.ASSIGNED: [Status.IN_PROGRESS, Status.ON_HOLD, Status.CLOSED],
    Status.IN_PROGRESS: [Status.ON_HOLD, Status.RESOLVED, Status.CLOSED],
    Status.ON_HOLD: [Status.IN_PROGRESS, Status.CLOSED],
    Status.RESOLVED: [Status.CLOSED, Status.IN_PROGRESS],
    Status.CLOSED: [Status.NEW, Status.IN_PROGRESS] # Allow reopening if needed
}
