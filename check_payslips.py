"""Check which employees have payslips"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.models.employee import Employee
from app.models.wage import WageStatement
from app.models.user import User

db = SessionLocal()

try:
    print("=" * 80)
    print("CHECKING EMPLOYEES AND THEIR PAYSLIPS")
    print("=" * 80)

    # Get all employees
    employees = db.query(Employee).filter(Employee.status == 'ACTIVE').all()

    print(f"\nTotal Active Employees: {len(employees)}")
    print("-" * 80)

    for emp in employees:
        print(f"\nEmployee ID: {emp.id}")
        print(f"  Code: {emp.employee_code}")
        print(f"  Name: {emp.first_name} {emp.last_name}")
        print(f"  Email: {emp.email}")

        # Check if employee has a user account
        user = db.query(User).filter(User.email == emp.email).first()
        if user:
            print(f"  User Account: Yes (username: {user.username}, role: {user.role})")
        else:
            print(f"  User Account: No")

        # Check payslips
        payslips = db.query(WageStatement).filter(
            WageStatement.employee_id == emp.id
        ).all()

        print(f"  Payslips: {len(payslips)}")
        if payslips:
            for ps in payslips:
                print(f"    - {ps.month}/{ps.year}: Rs.{ps.net_salary:,.2f} (status: {ps.status})")

    print("\n" + "=" * 80)
    print("WAGE STATEMENTS SUMMARY")
    print("=" * 80)

    all_statements = db.query(WageStatement).all()
    print(f"\nTotal Wage Statements: {len(all_statements)}")

    for stmt in all_statements:
        emp = db.query(Employee).filter(Employee.id == stmt.employee_id).first()
        emp_code = emp.employee_code if emp else f"ID:{stmt.employee_id}"
        print(f"  {emp_code} - {stmt.month}/{stmt.year}: Rs.{stmt.net_salary:,.2f} (status: {stmt.status})")

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
