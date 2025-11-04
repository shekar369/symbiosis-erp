class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(AppException):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppException):
    """Authorization failed"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)


class ResourceNotFoundError(AppException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppException):
    """Validation error"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)


class TenantNotFoundError(ResourceNotFoundError):
    """Tenant not found"""
    def __init__(self, message: str = "Tenant not found"):
        super().__init__(message)


class EmployeeNotFoundError(ResourceNotFoundError):
    """Employee not found"""
    def __init__(self, message: str = "Employee not found"):
        super().__init__(message)
