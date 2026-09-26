import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.routes.health import router as health_router
from app.routes.requests import router as requests_router

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("nie_servicehub.main")

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## NIE College Service Request System API

Production-ready REST API backend built with FastAPI, Pydantic v2, and MongoDB for managing campus service requests across departments:
- 📜 **Bonafide Certificate** (`BONAFIDE`)
- 🆔 **ID Card Services** (`ID_CARD`)
- 🏠 **Hostel Services** (`HOSTEL`)
- 🚌 **Transport Services** (`TRANSPORT`)
- 📚 **Library Services** (`LIBRARY`)
- 💻 **IT Support** (`IT_SUPPORT`)

### Request Lifecycle Flow
`NEW` ➔ `ASSIGNED` ➔ `IN_PROGRESS` ↔ `ON_HOLD` ➔ `RESOLVED` ➔ `CLOSED`
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Register API Routers
app.include_router(health_router, prefix="/api")
app.include_router(requests_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "project": "NIE ServiceHub",
        "description": "College Service Request System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "online"
    }

# Validation Error Handler (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field_name = " -> ".join([str(loc) for loc in err.get("loc", [])])
        errors.append({
            "field": field_name,
            "message": err.get("msg"),
            "type": err.get("type")
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "The request payload failed validation rules.",
            "details": errors
        }
    )

# Internal Server Error Handler (500) - Sanitized Response
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected server error occurred. Please try again later."
        }
    )
