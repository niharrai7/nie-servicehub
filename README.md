# NIE College Service Request System (NIE ServiceHub)

A centralized web application for college students and faculty at NIE to raise, track, and manage campus service requests efficiently across departments.

---

## 📌 Project Overview
**NIE ServiceHub** streamlines campus operations by replacing fragmented request methods with a structured service request workflow:
`Student / Faculty` → `Raise Request` → `Department Routing` → `Staff Assignment` → `In Progress Work` → `Resolution` → `Student Confirmation` → `Closed`

Supported Service Categories:
- 📜 **Bonafide Certificate** (`BONAFIDE`)
- 🆔 **ID Card Services** (`ID_CARD`)
- 🏠 **Hostel Services** (`HOSTEL`)
- 🚌 **Transport Services** (`TRANSPORT`)
- 📚 **Library Services** (`LIBRARY`)
- 💻 **IT Support Services** (`IT_SUPPORT`)

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.14+, JavaScript (ES6+) |
| **Backend Framework** | FastAPI (ASGI / Uvicorn) |
| **Data Validation** | Pydantic v2 |
| **Database** | MongoDB (PyMongo / Motor) |
| **API Testing** | Postman / Thunder Client |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
nie-servicehub/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI Application Entry Point & Exception Handlers
│   │   ├── config.py            # Environment Settings
│   │   ├── database.py          # MongoDB Database Connection Manager
│   │   ├── models/
│   │   │   └── service_request.py # Domain Enums (Category, Priority, Status, Lifecycle)
│   │   ├── schemas/
│   │   │   └── service_request.py # Pydantic Request/Response Validation Schemas
│   │   ├── routes/
│   │   │   ├── health.py        # Health Check Router (/api/health)
│   │   │   └── requests.py      # Service Request REST Routers (/api/requests)
│   │   ├── services/
│   │   │   └── request_service.py # Business Logic & MongoDB Query Layer
│   │   └── utils/               # Helpers & Utilities
│   ├── requirements.txt         # Python Dependencies
│   └── tests/
│       ├── test_db.py           # Database Connection Test Suite
│       └── test_requests.py     # Automated REST API Test Suite (12 Tests)
├── postman/
│   └── NIE-ServiceHub-Day2.postman_collection.json # Postman Collection
├── .env.example                 # Sample Environment Configuration
├── .gitignore                   # Git Ignore Configuration
└── README.md                    # Project Documentation
```

---

## ⚙️ Setup & Execution Instructions

### 1. Environment Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Automated API Tests
```bash
python -m unittest tests/test_requests.py
```

### 3. Run FastAPI Backend Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 📡 REST API Specification

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/api/health` | Health check & MongoDB connection status | 200 OK |
| `POST` | `/api/requests` | Raise a new service request | 201 Created |
| `GET` | `/api/requests` | List service requests (supports `status`, `category`, `priority`, `search`) | 200 OK |
| `GET` | `/api/requests/{request_id}` | Retrieve details for a single request | 200 OK / 404 |
| `PUT` | `/api/requests/{request_id}` | Update title, description, category, priority | 200 OK / 404 |
| `PATCH` | `/api/requests/{request_id}/status` | Update lifecycle status (NEW → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED) | 200 OK / 400 |
| `PATCH` | `/api/requests/{request_id}/assign` | Assign staff member & department (auto-updates status to ASSIGNED if NEW) | 200 OK / 404 |
| `DELETE` | `/api/requests/{request_id}` | Delete service request | 204 No Content |

---

## 📊 Learning Roadmap Status

- [x] **Day 1 — Foundation**: Git, GitHub, Python, MongoDB, Environment Setup, API Foundation
- [x] **Day 2-3 — FastAPI Backend**: Request Lifecycle, Pydantic Validation, Full REST Endpoints, Postman Collection, Automated Tests
- [ ] **Day 4-5 — React Frontend**: Dashboard, Request Forms, Routing, Bootstrap UI
- [ ] **Dockerization**: Dockerfiles, Docker Compose Orchestration
- [ ] **Day 6 — GenAI Integration**: AI-Assisted Ticket Classification & Recommendation
