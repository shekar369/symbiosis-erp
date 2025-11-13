"""
Quick script to check employee status in database
"""
import os
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

from app.db.session import SessionLocal
from app.models.employee import Employee

db = SessionLocal()

try:
    employees = db.query(Employee).order_by(Employee.id).all()

    print("=" * 80)
    print("EMPLOYEE STATUS CHECK")
    print("=" * 80)
    print(f"\nTotal Employees: {len(employees)}\n")

    print(f"{'ID':<5} {'Code':<10} {'Name':<30} {'Status':<15}")
    print("-" * 80)

    active_count = 0
    for emp in employees:
        full_name = f"{emp.first_name} {emp.last_name}"
        print(f"{emp.id:<5} {emp.employee_code:<10} {full_name:<30} {emp.status:<15}")
        if emp.status == "ACTIVE":
            active_count += 1

    print("\n" + "=" * 80)
    print(f"Active Employees: {active_count}")
    print(f"Total Employees: {len(employees)}")
    print("=" * 80)

finally:
    db.close()
