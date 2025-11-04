import logging
import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import IntegrityError, DatabaseError

from app.core.errors import AppException
from app.schemas.error import ErrorResponse

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except AppException as exc:
            request_id = str(uuid.uuid4())
            logger.error(
                f"Application error [{request_id}]: {exc.detail}",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "error_code": exc.error_code
                }
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorResponse(
                    error=exc.detail,
                    request_id=request_id,
                    details=[{"code": exc.error_code, "message": exc.detail}] if exc.error_code else None
                ).dict()
            )
        except IntegrityError as exc:
            request_id = str(uuid.uuid4())
            logger.error(
                f"Database integrity error [{request_id}]: {str(exc)}",
                extra={"request_id": request_id, "path": request.url.path},
                exc_info=True
            )
            error_message = "Database constraint violation"
            if "unique" in str(exc).lower():
                error_message = "A record with these values already exists"
            elif "foreign key" in str(exc).lower():
                error_message = "Referenced record does not exist"

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=ErrorResponse(
                    error=error_message,
                    request_id=request_id,
                    details=[{"code": "INTEGRITY_ERROR", "message": str(exc.orig)}]
                ).dict()
            )
        except DatabaseError as exc:
            request_id = str(uuid.uuid4())
            logger.critical(
                f"Database error [{request_id}]: {str(exc)}",
                extra={"request_id": request_id, "path": request.url.path},
                exc_info=True
            )
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=ErrorResponse(
                    error="Database service temporarily unavailable",
                    request_id=request_id
                ).dict()
            )
        except Exception as exc:
            request_id = str(uuid.uuid4())
            logger.critical(
                f"Unhandled exception [{request_id}]: {str(exc)}",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "exception_type": type(exc).__name__
                },
                exc_info=True
            )
            from app.config import settings
            error_detail = str(exc) if settings.ENVIRONMENT != "production" else "An internal error occurred"

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ErrorResponse(
                    error=error_detail,
                    request_id=request_id,
                    details=[{"code": "INTERNAL_ERROR", "message": "Please contact support with this request ID"}]
                ).dict()
            )
