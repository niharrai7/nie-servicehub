from fastapi import FastAPI
from app.config import settings
from app.database import get_database

app = FastAPI(
    title=settings.APP_NAME,
    description="NIE College Service Request System API - Step-by-Step Learning Project",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {
        "project": "NIE ServiceHub",
        "description": "College Service Request System",
        "status": "online",
        "learning_phase": "Day 1 - Foundation"
    }

@app.get("/api/health")
def health_check():
    db_status = "disconnected"
    try:
        db = get_database()
        # Test MongoDB connection by running ping command
        db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "database_name": settings.MONGO_DB_NAME
    }
