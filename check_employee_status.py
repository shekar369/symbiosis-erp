"""Check employee status values in database"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.models.employee import Employee, EmployeeStatus
from sqlalchemy import inspect

db = SessionLocal()

try:
    # Get column info
    inspector = inspect(db.bind)
    columns = inspector.get_columns('employees')

    status_col = [c for c in columns if c['name'] == 'status'][0]
    print(f"Status column type: {status_col['type']}")
    print(f"Nullable: {status_col['nullable']}")
    print(f"Default: {status_col.get('default')}")

    # Get actual status values
    print("\nEmployee status values:")
    employees = db.query(Employee.id, Employee.first_name, Employee.last_name, Employee.status).limit(15).all()

    for emp in employees:
        print(f"  ID {emp.id}: {emp.first_name} {emp.last_name} - Status: '{emp.status}' (type: {type(emp.status).__name__})")

    # Check EmployeeStatus enum
    print(f"\nEmployeeStatus enum values:")
    print(f"  ACTIVE: '{EmployeeStatus.ACTIVE.value}'")
    print(f"  INACTIVE: '{EmployeeStatus.INACTIVE.value}'")
    print(f"  TERMINATED: '{EmployeeStatus.TERMINATED.value}'")

finally:
    db.close()
