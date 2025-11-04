import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.models.user import User
from app.models.tenant import Tenant
from app.core.security import get_password_hash

# Use the same database URL as Alembic
engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_data():
    db = SessionLocal()
    try:
        # Create a test tenant
        existing_tenant = db.query(Tenant).filter(Tenant.slug == "it-solutions").first()
        if existing_tenant:
            tenant = existing_tenant
        else:
            tenant = Tenant(
                name="IT Solutions Ltd",
                slug="it-solutions",
                email="admin@it-solutions.com",
                phone="1234567890",
                address="123 Tech Street",
                is_active=True
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        # Create a SaasAdmin user
        saas_admin = db.query(User).filter(User.username == "saasadmin").first()
        if not saas_admin:
            saas_admin = User(
                username="saasadmin",
                email="admin@saas-payroll.com",
                hashed_password=get_password_hash("admin123"),
                full_name="SaaS Admin",
                role="saasadmin",
                is_active=True,
                is_superuser=True
            )
            db.add(saas_admin)

        # Create an employer user for the tenant
        employer = db.query(User).filter(User.username == "employer").first()
        if not employer:
            employer = User(
                username="employer",
                email="employer@it-solutions.com",
                hashed_password=get_password_hash("employer123"),
                full_name="IT Solutions HR Manager",
                role="employer",
                is_active=True,
                tenant_id=tenant.id
            )
            db.add(employer)

        # Create a test employee user
        employee = db.query(User).filter(User.username == "employee1").first()
        if not employee:
            employee = User(
                username="employee1",
                email="employee1@it-solutions.com",
                hashed_password=get_password_hash("employee123"),
                full_name="John Employee",
                role="employee",
                is_active=True,
                tenant_id=tenant.id
            )
            db.add(employee)

        db.commit()

    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test data...")
    create_test_data()
    print("Test data creation completed.")