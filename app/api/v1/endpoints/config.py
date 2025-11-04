from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_superuser
from app.crud import config as config_crud
from app.models.user import User
from app.schemas.config import (
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigResponse,
    ConfigCategory
)

router = APIRouter()


@router.post("/", response_model=SystemConfigResponse)
def create_system_config(
    config_in: SystemConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Create a new system configuration (superuser only)"""
    return config_crud.create_config(db, config_in)


@router.get("/{config_id}", response_model=SystemConfigResponse)
def get_system_config(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get a system configuration by ID (superuser only)"""
    config = config_crud.get_config(db, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config


@router.get("/key/{key}", response_model=SystemConfigResponse)
def get_config_by_key(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get a system configuration by key (superuser only)"""
    config = config_crud.get_config_by_key(db, key)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config


@router.get("/category/{category}", response_model=List[SystemConfigResponse])
def get_configs_by_category(
    category: ConfigCategory,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get system configurations by category (superuser only)"""
    return config_crud.get_configs_by_category(db, category, skip, limit)


@router.get("/", response_model=List[SystemConfigResponse])
def get_all_configs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get all system configurations (superuser only)"""
    return config_crud.get_all_configs(db, skip, limit)


@router.patch("/{config_id}", response_model=SystemConfigResponse)
def update_system_config(
    config_id: int,
    config_update: SystemConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update a system configuration (superuser only)"""
    config = config_crud.get_config(db, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config_crud.update_config(db, config, config_update)


@router.patch("/", response_model=List[SystemConfigResponse])
def bulk_update_configs(
    updates: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update multiple system configurations at once (superuser only)"""
    return config_crud.bulk_update_configs(db, updates)


@router.post("/initialize")
def initialize_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Initialize default system configurations (superuser only)"""
    config_crud.initialize_default_configs(db)
    return {"message": "Default configurations initialized successfully"}