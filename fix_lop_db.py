"""Fix Loss of Pay leave balance in database"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.models.leave import LeaveBalance, LeaveType
from sqlalchemy import update

db = SessionLocal()

try:
    # Get LOP leave type
    lop_type = db.query(LeaveType).filter(LeaveType.name == "Loss of Pay").first()

    if lop_type:
        print(f"Found Leave Type: {lop_type.name} (ID: {lop_type.id})")
        print(f"Current days_per_year: {lop_type.days_per_year}")

        # Update leave type
        lop_type.days_per_year = 0
        db.commit()
        print(f"[OK] Updated Leave Type days_per_year to 0")

        # Get all LOP balances
        lop_balances = db.query(LeaveBalance).filter(LeaveBalance.leave_type_id == lop_type.id).all()

        print(f"\nFound {len(lop_balances)} LOP leave balances")

        for balance in lop_balances:
            print(f"\nEmployee ID {balance.employee_id}:")
            print(f"  Before: total={balance.total_days}, used={balance.used_days}, balance={balance.balance_days}")

            balance.total_days = 0
            balance.balance_days = 0
            # Keep used_days as is (tracks actual LOP taken)

            print(f"  After: total={balance.total_days}, used={balance.used_days}, balance={balance.balance_days}")

        db.commit()
        print(f"\n[OK] Updated {len(lop_balances)} LOP balances successfully")

    else:
        print("Loss of Pay leave type not found")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()

print("\nDone!")
