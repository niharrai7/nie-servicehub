# NIE College Service Request System (NIE ServiceHub)

A production-ready centralized web application for college students and faculty at NIE to raise, track, and manage campus service requests efficiently across departments.

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
| **Containerization** | Docker / Dockerfile |
| **API Testing** | Postman / Thunder Client / unittest |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
nie-servicehub/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI Entry Point, OpenAPI Metadata & Global Exception Handlers
│   │   ├── config.py            # Environment Settings (MONGODB_URI, MONGODB_DATABASE, PORT)
│   │   ├── database.py          # MongoDB PyMongo Connection Manager
│   │   ├── models/
│   │   │   └── service_request.py # Domain Enums (Category, Priority, Status, Lifecycle Matrix)
│   │   ├── schemas/
│   │   │   └── service_request.py # Pydantic v2 Validation Schemas (whitespace & constraint checks)
│   │   ├── routes/
│   │   │   ├── health.py        # Health Diagnostic Router (/api/health)
│   │   │   └── requests.py      # Service Request REST Routers (/api/requests)
│   │   ├── services/
│   │   │   └── request_service.py # Business Logic & MongoDB Query Layer
│   │   └── utils/               # Helper utilities
│   ├── tests/
│   │   ├── test_db.py           # Database Connection Test Suite
│   │   └── test_requests.py     # 14 Automated REST API Tests
│   ├── Dockerfile               # Production Docker container definition
│   ├── .dockerignore            # Excluded build artifacts for Docker
│   └── requirements.txt         # Python Dependencies
├── postman/
│   ├── NIE-ServiceHub-Day2.postman_collection.json # Day 2 Postman Collection
│   └── NIE-ServiceHub-Day3.postman_collection.json # Day 3 Postman Collection
├── .env.example                 # Sample Environment Configuration
├── .gitignore                   # Git Ignore Rules
└── README.md                    # Project Documentation
```

---

## ⚙️ Setup & Execution Instructions

### 1. Local Environment Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Automated API Tests
```bash
python -m unittest tests/test_requests.py
```

### 3. Run FastAPI Backend Server Locally
```bash
python -m uvicorn app.main:app --reload --port 8000
```
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 🐳 Docker Deployment Instructions

### 1. Build the Docker Image
From the project root directory:
```bash
docker build -t nie-servicehub-backend ./backend
```

### 2. Run Backend Container
```bash
docker run -d -p 8000:8000 --name nie-backend -e MONGODB_URI=mongodb://host.docker.internal:27017 -e MONGODB_DATABASE=nie_servicehub nie-servicehub-backend
```

Access containerized health check:
```bash
curl http://localhost:8000/api/health
```

---

## 📡 REST API Specification

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/api/health` | Health check & MongoDB connection status | 200 OK |
| `POST` | `/api/requests` | Raise a new service request | 201 Created |
| `GET` | `/api/requests` | List requests (supports `status`, `category`, `priority`, `search`) | 200 OK |
| `GET` | `/api/requests/{request_id}` | Retrieve details for a single request | 200 OK / 404 |
| `PUT` | `/api/requests/{request_id}` | Update title, description, category, priority | 200 OK / 404 |
| `PATCH` | `/api/requests/{request_id}/status` | Update lifecycle status (NEW → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED) | 200 OK / 400 |
| `PATCH` | `/api/requests/{request_id}/assign` | Assign staff member & department (auto-updates status to ASSIGNED if NEW) | 200 OK / 404 |
| `DELETE` | `/api/requests/{request_id}` | Delete service request | 204 No Content |

---

## 🧪 Postman Testing Guide

Import [`postman/NIE-ServiceHub-Day3.postman_collection.json`](file:///c:/Users/Nihar/Documents/7845/postman/NIE-ServiceHub-Day3.postman_collection.json) into Postman or Thunder Client to execute the complete verification sequence:
1. Health Check (`GET /api/health`)
2. Create Request (`POST /api/requests`)
3. List Requests (`GET /api/requests`)
4. Filter Requests (`GET /api/requests?category=ID_CARD&status=NEW`)
5. Get Single Request (`GET /api/requests/REQ-1001`)
6. Update Request (`PUT /api/requests/REQ-1001`)
7. Assign Staff (`PATCH /api/requests/REQ-1001/assign`)
8. Change Status (`PATCH /api/requests/REQ-1001/status`)
9. Test Invalid Status Transition (`PATCH /api/requests/REQ-1001/status`)
10. Test Non-Existent Request (`GET /api/requests/REQ-9999`)
11. Test Validation Failure (`POST /api/requests`)
12. Delete Request (`DELETE /api/requests/REQ-1001`)

---

## 📊 Learning Roadmap Status

- [x] **Day 1 — Foundation**: Git, GitHub, Python, MongoDB, Environment Setup, API Foundation
- [x] **Day 2-3 — FastAPI Backend Completion & Docker**: Request Lifecycle, Schemas, Robust Error Handling, Postman Collections, 14 Automated Tests, Dockerfile
- [ ] **Day 4-5 — React Frontend**: Dashboard, Request Forms, Routing, Bootstrap UI
- [ ] **Dockerization**: Dockerfiles, Docker Compose Orchestration
- [ ] **Day 6 — GenAI Integration**: AI-Assisted Ticket Classification & Recommendation
