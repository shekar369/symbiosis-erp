from typing import List
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings
import json
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "HR Payroll System - Symbiosis"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Database - PostgreSQL
    DATABASE_URL: str = "postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000","http://localhost:5174","http://localhost:5173", "http://localhost:8000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = [".xlsx", ".xls", ".csv"]
    UPLOAD_DIR: str = "uploads"
    
    # Email
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
