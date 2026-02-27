from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import todos
from .core.exceptions import AppException
from .core.error_response import ErrorResponse

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="Todo API with API Key auth, clean error handling",
    version="1.0.0",
    redirect_slashes=False
)

# ─── CORS ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Exception Handlers ───────────────────────────────

# Our custom AppException and all subclasses
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    # Map business/app exceptions to appropriate HTTP status
    status_map = {
        2001: 401,  # Unauthorized
        2002: 403,  # Forbidden
        2003: 404,  # Not Found
        2004: 409,  # Conflict
        2005: 422,  # Validation
        2006: 429,  # Rate Limit
        3001: 404,  # TodoNotFound
        3002: 400,  # AlreadyCompleted
        3003: 400,  # TitleEmpty
        3004: 400,  # LimitExceeded
    }
    http_status = status_map.get(exc.code, 400)

    return JSONResponse(
        status_code=http_status,
        content=ErrorResponse(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        ).model_dump(exclude_none=True),
    )

# Pydantic validation errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code=2005,
            message="Validation failed",
            errors={"detail": exc.errors()},
        ).model_dump(exclude_none=True),
    )

# Catch all unexpected errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code=2000,
            message="Internal server error",
            details=str(exc),
        ).model_dump(exclude_none=True),
    )

# ─── Routers ──────────────────────────────────────────
app.include_router(todos.router)

# ─── Health ───────────────────────────────────────────
@app.get("/", tags=["health"])
def root():
    return {"message": "Todo API is running", "version": "1.0.0"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}