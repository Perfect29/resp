"""HTTP error handlers and exceptions."""

import logging
from typing import Any, Optional

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, id: str):
        """
        Initialize NotFoundError.

        Args:
            resource: Resource type (e.g., "target")
            id: Resource ID
        """
        self.resource = resource
        self.id = id
        self.message = f"{resource.capitalize()} with id '{id}' not found"
        super().__init__(self.message)


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """
    Handle NotFoundError exceptions.

    Args:
        request: FastAPI request object
        exc: NotFoundError exception

    Returns:
        JSON error response
    """
    logger.warning(f"Not found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Not Found", "detail": exc.message},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Args:
        request: FastAPI request object
        exc: RequestValidationError exception

    Returns:
        JSON error response
    """
    errors = exc.errors()
    error_messages = []

    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        message = error.get("msg", "Validation error")
        error_messages.append(f"{field}: {message}")

    error_detail = "; ".join(error_messages)
    logger.warning(f"Validation error: {error_detail}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation Error", "detail": error_detail},
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handle HTTP exceptions.

    Args:
        request: FastAPI request object
        exc: StarletteHTTPException exception

    Returns:
        JSON error response
    """
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Error", "detail": str(exc.detail)},
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Args:
        request: FastAPI request object
        exc: Exception

    Returns:
        JSON error response
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
        },
    )





