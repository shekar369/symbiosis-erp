import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

# Create SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import test models
from test_models import Base, User, SystemConfig

Base.metadata.create_all(bind=engine)

def create_test_data():
    db = SessionLocal()
    try:
        # Create SaaS Admin user with simple password hashing
        saas_admin = User(
            username="saasadmin",
            email="admin@hrpayroll.com",
            hashed_password=hashlib.sha256("admin123".encode()).hexdigest(),
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
                "description": "SMTP server host",
                "category": "EMAIL",
                "is_active": True,
            },
            {
                "key": "EMAIL_PORT",
                "value": "587",
                "description": "SMTP server port",
                "category": "EMAIL",
                "is_active": True,
            },
            {
                "key": "SYSTEM_TIMEZONE",
                "value": "UTC",
                "description": "System timezone",
                "category": "SYSTEM",
                "is_active": True,
            }
        ]

        for config in test_configs:
            db_config = SystemConfig(**config)
            db.add(db_config)

        db.commit()
        print("Successfully created test data!")
        print("\nLogin credentials:")
        print("Username: saasadmin")
        print("Password: admin123")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()