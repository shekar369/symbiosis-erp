from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ErrorDetail(BaseModel):
    """Standard error detail structure"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response structure"""
    success: bool = False
    error: str
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = None


class ValidationErrorResponse(ErrorResponse):
    """Validation error response with field-level errors"""
    validation_errors: Dict[str, List[str]]


class SuccessResponse(BaseModel):
    """Standard success response structure"""
    success: bool = True
    message: str
    data: Optional[Any] = None
