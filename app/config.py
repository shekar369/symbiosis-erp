from typing import List, Optional, Union
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings
import json
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "HR Payroll System - Symbiosis"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production

    @field_validator('API_V1_STR', mode='before')
    @classmethod
    def ensure_api_path(cls, v):
        # Ensure API path always starts with / even if env parsing changes it
        if v and not str(v).startswith('/'):
            # Handle Git Bash path conversion (C:/Program Files/Git/api/v1 -> /api/v1)
            parts = str(v).split('/')
            if len(parts) >= 2:
                return f"/{parts[-2]}/{parts[-1]}"  # Get last two parts
            return f"/{parts[-1]}"
        return v or "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll"

    # Security - Generate secure default but require override in production
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v, info: ValidationInfo):
        """Ensure SECRET_KEY is secure in production"""
        environment = info.data.get("ENVIRONMENT", "development")

        if environment == "production":
            if not v or len(v) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            # Check for common weak keys
            weak_keys = [
                "your-secret-key-change-this-in-production",
                "changeme",
                "secret",
                "password",
                "12345"
            ]
            if any(weak in v.lower() for weak in weak_keys):
                raise ValueError(
                    "Weak SECRET_KEY detected in production. "
                    "You MUST set a secure SECRET_KEY via environment variable."
                )

        return v

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000","http://localhost:5174","http://localhost:5173", "http://localhost:8000"]

    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".xlsx", ".xls", ".csv"]
    UPLOAD_DIR: str = "uploads"

    # Email Configuration
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Symbiosis HR Payroll System"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
