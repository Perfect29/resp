"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.targets import router as targets_router
from app.errors.http_errors import (
    NotFoundError,
    general_exception_handler,
    http_exception_handler,
    not_found_handler,
    validation_exception_handler,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.

    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting AI Visibility Tracker API")
    yield
    # Shutdown
    logger.info("Shutting down AI Visibility Tracker API")


# Create FastAPI app
app = FastAPI(
    title="AI Visibility Tracker API",
    description="MVP backend for tracking business visibility across AI platforms",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register routers
app.include_router(targets_router)


@app.get("/", response_class=JSONResponse)
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "AI Visibility Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_class=JSONResponse)
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}
