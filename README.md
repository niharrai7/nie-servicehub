# NIE College Service Request System (NIE ServiceHub)

A centralized web application for college students and faculty at NIE to raise, track, and manage campus service requests efficiently across departments.

---

## 📌 Project Overview
**NIE ServiceHub** streamilnes campus operations by replacing fragmented request methods with a structured service request workflow:
`Student / Faculty` → `Raise Request` → `Department Routing` → `Staff Assignment` → `In Progress Work` → `Resolution` → `Student Confirmation` → `Closed`

Supported Service Categories:
- 📜 **Bonafide Certificate**
- 🆔 **ID Card Services**
- 🏠 **Hostel Services**
- 🚌 **Transport Services**
- 📚 **Library Services**
- 💻 **IT Support Services**

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.14+, JavaScript (ES6+) |
| **Backend Framework** | FastAPI |
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
│   │   ├── main.py              # FastAPI Application Entry Point
│   │   ├── config.py            # Environment Configuration
│   │   ├── database.py          # MongoDB Database Connection Manager
│   │   ├── models/              # Data Models
│   │   ├── schemas/             # Pydantic Validation Schemas
│   │   ├── routes/              # REST API Routes
│   │   ├── services/            # Business Logic Layer
│   │   └── utils/               # Utility Functions
│   ├── requirements.txt         # Python Dependencies
│   └── tests/
│       └── test_db.py           # MongoDB Connectivity Test Suite
├── .env.example                 # Sample Environment Configuration
├── .gitignore                   # Git Ignore Configuration
└── README.md                    # Project Documentation
```

---

## ⚙️ Setup Instructions (Day 1 - Foundation)

### Prerequisites
- Python 3.10+
- MongoDB installed locally or MongoDB Cloud Connection String
- Git

### 1. Clone & Configure Remote
```bash
git clone https://github.com/niharrai7/nie-servicehub.git
cd nie-servicehub
```

### 2. Environment Setup
Create a `.env` file in the project root:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=nie_servicehub
APP_NAME="NIE ServiceHub API"
DEBUG=True
PORT=8000
```

### 3. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Verify Database Connection
Run the database test script to verify Python → MongoDB connectivity:
```bash
python tests/test_db.py
```

### 5. Run FastAPI Application
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Access API Documentation (Swagger): `http://127.0.0.1:8000/docs`

---

## 📡 Initial REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Application Root & Status Info |
| `GET` | `/api/health` | Service & Database Health Check |

---

## 📊 Learning Roadmap Status

- [x] **Day 1 — Foundation**: Git, GitHub, Python, MongoDB, Environment Setup, API Foundation
- [ ] **Day 2-3 — FastAPI Backend**: Request Lifecycle, Schemas, Full REST Endpoints, Auth
- [ ] **Day 4-5 — React Frontend**: Dashboard, Request Forms, Routing, Bootstrap UI
- [ ] **Dockerization**: Dockerfiles, Docker Compose Orchestration
- [ ] **Day 6 — GenAI Integration**: AI-Assisted Ticket Classification & Recommendation
