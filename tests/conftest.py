import itertools
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_db
from app.core.security import get_password_hash
from app.db.base import Base
from app.main import app
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.rollback()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def test_tenant(db):
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


_DEFAULT_TENANT = object()


@pytest.fixture()
def user_factory(db, test_tenant):
    counter = itertools.count(1)

    def _factory(
        *,
        username: str | None = None,
        email: str | None = None,
        password: str = "TestPass123!",
        role: str = "employee",
        is_active: bool = True,
        is_superuser: bool = False,
        tenant_id: int | None | object = _DEFAULT_TENANT
    ) -> tuple[User, str]:
        idx = next(counter)
        username = username or f"user{idx}"
        email = email or f"{username}@example.com"
        hashed_password = get_password_hash(password)

        tenant_value = test_tenant.id if tenant_id is _DEFAULT_TENANT else tenant_id

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=is_active,
            is_superuser=is_superuser,
            tenant_id=tenant_value
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, password

    return _factory


@pytest.fixture()
def auth_headers(client, user_factory):
    def _create_and_login(**user_kwargs):
        user, password = user_factory(**user_kwargs)
        response = client.post(
            "/api/v1/auth/login",
            data={"username": user.username, "password": password}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        return user, {"Authorization": f"Bearer {token}"}

    return _create_and_login


@pytest.fixture()
def test_employee(db, test_tenant):
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
    return employee
