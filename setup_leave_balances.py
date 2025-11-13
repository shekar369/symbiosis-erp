"""
Setup leave balances for all employees based on their leave types
"""
import os
import sys
from datetime import datetime

# Ensure DATABASE_URL is not set in environment
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.leave import LeaveType, LeaveBalance
from app.models.employee import Employee
from app.models.tenant import Tenant

def setup_leave_balances():
    db: Session = SessionLocal()
    current_year = datetime.now().year

    try:
        print("=" * 70)
        print("SETTING UP LEAVE BALANCES FOR EMPLOYEES")
        print("=" * 70)

        # Get all tenants
        tenants = db.query(Tenant).all()

        if not tenants:
            print("\n[ERROR] No tenants found.")
            return False

        total_balances_created = 0

        for tenant in tenants:
            print(f"\n\nTenant: {tenant.name} (ID: {tenant.id})")
            print("-" * 70)

            # Get all employees for this tenant
            employees = db.query(Employee).filter(
                Employee.tenant_id == tenant.id,
                Employee.status == "ACTIVE"
            ).all()

            if not employees:
                print(f"   [WARNING] No active employees found for tenant {tenant.name}")
                continue

            # Get all leave types for this tenant
            leave_types = db.query(LeaveType).filter(
                LeaveType.tenant_id == tenant.id
            ).all()

            if not leave_types:
                print(f"   [WARNING] No leave types found for tenant {tenant.name}")
                continue

            print(f"\n   Found {len(employees)} active employees and {len(leave_types)} leave types")
            print(f"   Creating leave balances for year {current_year}...\n")

            for employee in employees:
                emp_name = f"{employee.first_name} {employee.last_name}"
                print(f"   Employee: {emp_name} ({employee.employee_code})")

                for leave_type in leave_types:
                    # Check if balance already exists
                    existing_balance = db.query(LeaveBalance).filter(
                        LeaveBalance.employee_id == employee.id,
                        LeaveBalance.leave_type_id == leave_type.id,
                        LeaveBalance.year == current_year
                    ).first()

                    if existing_balance:
                        print(f"      [EXISTS] {leave_type.name}: {existing_balance.balance_days} days available")
                    else:
                        # Create new leave balance
                        leave_balance = LeaveBalance(
                            employee_id=employee.id,
                            leave_type_id=leave_type.id,
                            year=current_year,
                            total_days=leave_type.days_per_year,
                            used_days=0,
                            balance_days=leave_type.days_per_year
                        )
                        db.add(leave_balance)
                        total_balances_created += 1
                        print(f"      [CREATED] {leave_type.name}: {leave_type.days_per_year} days allocated")

                print()  # Empty line between employees

            db.commit()

        print("\n" + "=" * 70)
        print("LEAVE BALANCES SETUP COMPLETE!")
        print("=" * 70)
        print(f"\nTotal Leave Balances Created: {total_balances_created}")
        print(f"Year: {current_year}")
        print(f"\nEmployees can now apply for leaves!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = setup_leave_balances()
    if success:
        print("\n[SUCCESS] Leave balances setup completed!")
    else:
        print("\n[FAILED] Failed to setup leave balances.")
        sys.exit(1)
