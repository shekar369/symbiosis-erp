import sys
sys.path.append(".")

from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.organization import Department, Designation, Grade


def seed_data():
    db = SessionLocal()

    try:
        # Create sample tenant
        tenant = Tenant(
            name="Demo Company",
            slug="demo-company",
            email="demo@company.com",
            phone="1234567890",
            address="123 Demo Street"
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"Created tenant: {tenant.name}")

        # Create sample departments
        departments = [
            Department(tenant_id=tenant.id, name="Engineering", code="ENG", description="Engineering Department"),
            Department(tenant_id=tenant.id, name="HR", code="HR", description="Human Resources"),
            Department(tenant_id=tenant.id, name="Finance", code="FIN", description="Finance Department"),
        ]
        db.add_all(departments)
        db.commit()
        print(f"Created {len(departments)} departments")

        # Create sample designations
        designations = [
            Designation(tenant_id=tenant.id, name="Software Engineer", code="SE", description="Software Engineer"),
            Designation(tenant_id=tenant.id, name="HR Manager", code="HRM", description="HR Manager"),
            Designation(tenant_id=tenant.id, name="Accountant", code="ACC", description="Accountant"),
        ]
        db.add_all(designations)
        db.commit()
        print(f"Created {len(designations)} designations")

        # Create sample grades
        grades = [
            Grade(tenant_id=tenant.id, name="Junior", code="JR", description="Junior Level"),
            Grade(tenant_id=tenant.id, name="Senior", code="SR", description="Senior Level"),
            Grade(tenant_id=tenant.id, name="Lead", code="LD", description="Lead Level"),
        ]
        db.add_all(grades)
        db.commit()
        print(f"Created {len(grades)} grades")

        print("Seed data created successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
