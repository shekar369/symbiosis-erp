import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.main import app
from app.db.base import Base
from app.api.dependencies import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate
from app.models.employee import Employee

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}

@pytest.fixture
def test_tenant(db):
    # Create a test tenant
    tenant_data = TenantCreate(
        name="Test Company",
        slug="test-company",
        email="test@company.com",
        phone="1234567890",
        address="Test Address"
    )
    tenant = Tenant(
        name=tenant_data.name,
        slug=tenant_data.slug,
        email=tenant_data.email,
        phone=tenant_data.phone,
        address=tenant_data.address
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@pytest.fixture
def admin_token_headers(client: TestClient, test_users):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test_admin",
            "password": "test_admin_pass"
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
    db.refresh(tenant)
    yield tenant
    # Cleanup is handled by the db fixture

@pytest.fixture
def test_employee(db, test_tenant):
    # Create a test employee
    employee = Employee(
        tenant_id=test_tenant.id,
        employee_code="EMP001",
        first_name="John",
        last_name="Doe",
        email="john.doe@testcompany.com",
        phone="1234567890",
        date_of_birth=date(1990, 1, 1),
        date_of_joining=date(2020, 1, 1)
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    yield employee
    # Cleanup is handled by the db fixture

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
