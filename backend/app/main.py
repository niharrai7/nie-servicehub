from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.routes.health import router as health_router
from app.routes.requests import router as requests_router

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## NIE College Service Request System API

A REST API backend built with FastAPI, Pydantic, and MongoDB for managing campus service requests:
- 📜 **Bonafide Certificate**
- 🆔 **ID Card Services**
- 🏠 **Hostel Services**
- 🚌 **Transport Services**
- 📚 **Library Services**
- 💻 **IT Support**

### Request Lifecycle Progression
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

# Custom Validation Error Handler for clear 422 JSON response
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
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "The request payload failed validation rules.",
            "details": errors
        }
    )
