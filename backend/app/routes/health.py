from fastapi import APIRouter, status
from app.config import settings
from app.database import get_database

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Service & Database Health Check",
    description="Check the operational status of the API service and MongoDB database connection."
)
def health_check():
    db_status = "disconnected"
    try:
        db = get_database()
        db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "database_name": settings.MONGO_DB_NAME
    }
