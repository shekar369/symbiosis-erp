from typing import List, Optional, Dict, Any
import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.config import SystemConfig, DEFAULT_CONFIGS
from app.schemas.config import SystemConfigCreate, SystemConfigUpdate, ConfigCategory
from app.core.security import encrypt_value, decrypt_value


def initialize_default_configs(db: Session):
    """Initialize default system configurations if they don't exist"""
    for config_data in DEFAULT_CONFIGS:
        existing = get_config_by_key(db, config_data["key"])
        if not existing:
            # Make a copy to avoid modifying the original DEFAULT_CONFIGS
            config = config_data.copy()

            # If value needs encryption, serialize it first if it's not a string
            if config.get("is_encrypted") and config["value"]:
                value = config["value"]
                # Convert non-string values to JSON string before encryption
                if not isinstance(value, str):
                    value = json.dumps(value)
                config["value"] = encrypt_value(value)

            db_config = SystemConfig(**config)
            db.add(db_config)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error initializing default configurations"
        )


def create_config(db: Session, config: SystemConfigCreate) -> SystemConfig:
    """Create a new system configuration"""
    existing = get_config_by_key(db, config.key)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration with key '{config.key}' already exists"
        )

    value = config.value
    if config.is_encrypted and value:
        # Convert non-string values to JSON string before encryption
        if not isinstance(value, str):
            value = json.dumps(value)
        value = encrypt_value(value)

    db_config = SystemConfig(**config.model_dump(exclude={"value"}), value=value)
    db.add(db_config)
    try:
        db.commit()
        db.refresh(db_config)
        return db_config
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid configuration data"
        )


def get_config(db: Session, config_id: int) -> Optional[SystemConfig]:
    """Get a system configuration by ID"""
    return db.query(SystemConfig).filter(SystemConfig.id == config_id).first()


def get_config_by_key(db: Session, key: str) -> Optional[SystemConfig]:
    """Get a system configuration by key"""
    return db.query(SystemConfig).filter(SystemConfig.key == key).first()


def get_configs_by_category(
    db: Session,
    category: ConfigCategory,
    skip: int = 0,
    limit: int = 100
) -> List[SystemConfig]:
    """Get system configurations by category"""
    return db.query(SystemConfig)\
        .filter(SystemConfig.category == category)\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_all_configs(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[SystemConfig]:
    """Get all system configurations"""
    return db.query(SystemConfig).offset(skip).limit(limit).all()


def update_config(
    db: Session,
    config: SystemConfig,
    config_update: SystemConfigUpdate
) -> SystemConfig:
    """Update a system configuration"""
    update_data = config_update.model_dump(exclude_unset=True)
    
    if "value" in update_data and config.is_encrypted:
        value = update_data["value"]
        # Convert non-string values to JSON string before encryption
        if not isinstance(value, str):
            value = json.dumps(value)
        update_data["value"] = encrypt_value(value)
    
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.add(config)
    try:
        db.commit()
        db.refresh(config)
        return config
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid configuration update"
        )


def bulk_update_configs(
    db: Session,
    updates: Dict[str, Any]
) -> List[SystemConfig]:
    """Update multiple configurations at once"""
    updated_configs = []
    
    for key, value in updates.items():
        config = get_config_by_key(db, key)
        if not config:
            raise HTTPException(
                status_code=404,
                detail=f"Configuration '{key}' not found"
            )
        
        if config.is_encrypted:
            # Convert non-string values to JSON string before encryption
            if not isinstance(value, str):
                value = json.dumps(value)
            value = encrypt_value(value)
        
        config.value = value
        updated_configs.append(config)
        db.add(config)
    
    try:
        db.commit()
        for config in updated_configs:
            db.refresh(config)
        return updated_configs
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid configuration update"
        )


def get_config_value(config: SystemConfig) -> Any:
    """Get the decrypted value of a configuration"""
    if config.is_encrypted and config.value:
        decrypted = decrypt_value(config.value)
        # Try to parse as JSON if it was serialized
        try:
            return json.loads(decrypted)
        except (json.JSONDecodeError, TypeError):
            return decrypted
    return config.value