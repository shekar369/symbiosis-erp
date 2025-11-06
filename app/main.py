import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.api.v1.router import api_router
from app.config import settings
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate unique operation IDs for OpenAPI schema"""
    return f"{route.tags[0]}-{route.name}" if route.tags else route.name

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Symbiosis HR Payroll System API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    generate_unique_id_function=custom_generate_unique_id
)

# Set up CORS - Allow all origins in development for maximum compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # All HTTP methods
    allow_headers=["*"],  # All headers including Authorization, Content-Type
    expose_headers=["*"],  # Expose all response headers
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Symbiosis HR Payroll API", "version": "1.0.0"}
