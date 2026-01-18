"""Get all credentials from database for documentation"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.employee import Employee
from app.models.tenant import Tenant

def get_credentials():
    db = SessionLocal()

    try:
        print("=" * 80)
        print("HR PAYROLL SYSTEM - DATABASE CREDENTIALS")
        print("=" * 80)
        print()

        # Get tenants
        print("TENANTS:")
        print("-" * 80)
        tenants = db.query(Tenant).all()
        for tenant in tenants:
            print(f"ID: {tenant.id}")
            print(f"Name: {tenant.name}")
            print(f"Slug: {tenant.slug}")
            print(f"Email: {tenant.email}")
            print(f"Phone: {tenant.phone}")
            print(f"Active: {tenant.is_active}")
            print()

        # Get users
        print("\nUSERS (LOGIN CREDENTIALS):")
        print("-" * 80)
        users = db.query(User).order_by(User.role, User.id).all()

        for user in users:
            print(f"\nRole: {user.role.upper()}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Full Name: {user.full_name}")
            print(f"  Tenant ID: {user.tenant_id}")
            print(f"  Active: {user.is_active}")
            print(f"  NOTE: Password is hashed, use default test passwords:")
            if user.role == "employer_admin" or user.role == "employer":
                print(f"        Try: employer123")
            elif user.role == "employee":
                print(f"        Try: employee123")
            else:
                print(f"        Try: {user.role}123")

        # Get employees count
        print("\n\nEMPLOYEES:")
        print("-" * 80)
        employees = db.query(Employee).order_by(Employee.employee_code).limit(10).all()
        print(f"Total employees in database: {db.query(Employee).count()}")
        print(f"\nFirst 10 employees:")

        for emp in employees:
            print(f"\n  Code: {emp.employee_code}")
            print(f"  Name: {emp.first_name} {emp.last_name}")
            print(f"  Email: {emp.email}")
            print(f"  Department: {emp.department if hasattr(emp, 'department') else 'N/A'}")
            print(f"  Status: {emp.status}")
            print(f"  Tenant ID: {emp.tenant_id}")

            # Check if has salary details
            if hasattr(emp, 'salary_details') and emp.salary_details:
                print(f"  Basic Salary: Rs. {emp.salary_details.basic_salary:,.2f}")
                print(f"  CTC: Rs. {emp.salary_details.ctc:,.2f}")

        print("\n" + "=" * 80)
        print("DATABASE QUERY COMPLETED SUCCESSFULLY")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    get_credentials()
