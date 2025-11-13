"""Populate sample attendance data for all employees for last 2 months"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.models.employee import Employee
from app.models.attendance import Attendance
from datetime import datetime, timedelta, date
from calendar import monthrange
from sqlalchemy import extract

db = SessionLocal()

try:
    # Get current date
    current_date = datetime.now()

    # Calculate last 2 months
    last_month = current_date.replace(day=1) - timedelta(days=1)
    month_before_last = last_month.replace(day=1) - timedelta(days=1)

    months_to_process = [
        (month_before_last.month, month_before_last.year),
        (last_month.month, last_month.year)
    ]

    # Get all active employees
    employees = db.query(Employee).filter(Employee.status == 'ACTIVE').all()

    print(f"Found {len(employees)} active employees")
    print(f"Generating attendance for:")
    for month, year in months_to_process:
        month_name = datetime(year, month, 1).strftime("%B %Y")
        print(f"  - {month_name}")

    print("\n" + "=" * 80)

    total_records = 0

    for employee in employees:
        print(f"\nEmployee: {employee.first_name} {employee.last_name} ({employee.employee_code})")

        for month, year in months_to_process:
            total_days = monthrange(year, month)[1]
            month_name = datetime(year, month, 1).strftime("%B %Y")

            # Check if attendance already exists for this month
            existing_count = db.query(Attendance).filter(
                Attendance.employee_id == employee.id,
                extract('month', Attendance.date) == month,
                extract('year', Attendance.date) == year
            ).count()

            if existing_count > 0:
                print(f"  {month_name}: Already has {existing_count} attendance records, skipping")
                continue

            # Create attendance for each day of the month
            month_records = 0
            for day in range(1, total_days + 1):
                attendance_date = date(year, month, day)

                # Skip Sundays (assuming Sunday is weekly off)
                if attendance_date.weekday() == 6:
                    status = 'weekly_off'
                else:
                    # Mark everyone as present for simplicity
                    status = 'present'

                attendance = Attendance(
                    employee_id=employee.id,
                    date=attendance_date,
                    status=status,
                    hours_worked=8 if status == 'present' else 0
                )
                db.add(attendance)
                month_records += 1

            print(f"  {month_name}: Created {month_records} attendance records")
            total_records += month_records

    db.commit()
    print("\n" + "=" * 80)
    print(f"[OK] Successfully created {total_records} attendance records")
    print("=" * 80)

except Exception as e:
    db.rollback()
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print("\nDone!")
