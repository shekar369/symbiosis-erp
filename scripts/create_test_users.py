"""
Script to create test users for different roles in the system.
"""
import sys
from datetime import datetime
sys.path.append(".")

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.tenant import Tenant
from app.models.user import User
from app.core.constants import (
    ROLE_SAAS_ADMIN,
    ROLE_EMPLOYER_ADMIN,
    ROLE_EMPLOYEE,
    ROLE_AUDITOR
)

# Test user credentials
TEST_USERS = [
    {
        "username": "saas_admin",
        "email": "saas.admin@hrpayroll.com",
        "password": "SaasAdmin@2025#",
        "role": ROLE_SAAS_ADMIN,
        "is_superuser": True
    },
    {
        "username": "employer_admin",
        "email": "employer.admin@company.com",
        "password": "EmployerAdmin@2025#",
        "role": ROLE_EMPLOYER_ADMIN,
        "is_superuser": False
    },
    {
        "username": "employee_test",
        "email": "employee@company.com",
        "password": "Employee@2025#",
        "role": ROLE_EMPLOYEE,
        "is_superuser": False
    },
    {
        "username": "auditor_test",
        "email": "auditor@audit-firm.com",
        "password": "Auditor@2025#",
        "role": ROLE_AUDITOR,
        "is_superuser": False
    }
]

def create_test_tenant(db: Session) -> Tenant:
    """Create a test tenant if it doesn't exist"""
    tenant = db.query(Tenant).filter(Tenant.name == "Test Company").first()
    if not tenant:
        tenant = Tenant(
            name="Test Company",
            slug="test-company",
            email="admin@testcompany.com",
            phone="+1234567890",
            address="123 Test Street, Test City",
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
    return tenant

def create_test_users(db: Session, tenant: Tenant):
    """Create test users for different roles"""
    for user_data in TEST_USERS:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing_user:
            user = User(
                tenant_id=tenant.id,
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_active=True,
                is_superuser=user_data["is_superuser"],
                created_at=datetime.utcnow()
            )
            db.add(user)
    db.commit()

def main():
    """Main function to create test users"""
    db = SessionLocal()
    try:
        tenant = create_test_tenant(db)
        create_test_users(db, tenant)
        print("Test users created successfully!")
        print("\nTest User Credentials:")
        print("-" * 50)
        for user in TEST_USERS:
            print(f"\nRole: {user['role']}")
            print(f"Username: {user['username']}")
            print(f"Password: {user['password']}")
            print(f"Email: {user['email']}")
    finally:
        db.close()

if __name__ == "__main__":
    main()