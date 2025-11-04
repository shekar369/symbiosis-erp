import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.user import User
from app.models.config import SystemConfig
from app.core.security import get_password_hash, encrypt_value
from datetime import datetime

def setup_database():
    # Create tables
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create new tables

def create_test_saas_admin():
    setup_database()
    db = SessionLocal()
    try:
        # Create SaaS Admin user
        saas_admin = User(
            username="saasadmin",
            email="admin@hrpayroll.com",
            hashed_password=get_password_hash("admin123"),
            full_name="SaaS Administrator",
            role="saas_admin",
            is_active=True,
            is_superuser=True,
        )
        db.add(saas_admin)

        # Create test configurations
        test_configs = [
            {
                "key": "EMAIL_HOST",
                "value": "smtp.gmail.com",
                "description": "SMTP server host for sending emails",
                "category": "EMAIL",
                "is_encrypted": False,
                "is_active": True,
            },
            {
                "key": "EMAIL_PORT",
                "value": "587",
                "description": "SMTP server port",
                "category": "EMAIL",
                "is_encrypted": False,
                "is_active": True,
            },
            {
                "key": "EMAIL_PASSWORD",
                "value": "test_password",
                "description": "SMTP server password",
                "category": "EMAIL",
                "is_encrypted": True,
                "is_active": True,
            },
            {
                "key": "DEFAULT_TIMEZONE",
                "value": "UTC",
                "description": "System default timezone",
                "category": "SYSTEM",
                "is_encrypted": False,
                "is_active": True,
            },
            {
                "key": "JWT_SECRET",
                "value": "test_secret_key",
                "description": "Secret key for JWT token generation",
                "category": "SECURITY",
                "is_encrypted": True,
                "is_active": True,
            },
            {
                "key": "NOTIFICATION_ENABLED",
                "value": "true",
                "description": "Enable/disable system notifications",
                "category": "NOTIFICATION",
                "is_encrypted": False,
                "is_active": True,
            },
            {
                "key": "PAYMENT_GATEWAY_API_KEY",
                "value": "test_api_key",
                "description": "API key for payment gateway",
                "category": "BILLING",
                "is_encrypted": True,
                "is_active": True,
            },
        ]

        for config in test_configs:
            if config["is_encrypted"] and config["value"]:
                config["value"] = encrypt_value(config["value"])
            db_config = SystemConfig(**config)
            db.add(db_config)

        db.commit()
        print("Successfully created SaaS admin user and test configurations")
        print("\nLogin credentials:")
        print("Username: saasadmin")
        print("Password: saasadmin123")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_saas_admin()