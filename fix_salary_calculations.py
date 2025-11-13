"""Fix salary calculations for all employees"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.models.employee import EmployeeSalaryDetails

db = SessionLocal()

try:
    # Get all salary records
    salary_records = db.query(EmployeeSalaryDetails).all()

    print(f"Found {len(salary_records)} salary records to fix")
    print("=" * 80)

    fixed_count = 0
    for salary in salary_records:
        print(f"\nEmployee ID: {salary.employee_id}")

        # Store old values
        old_gross = float(salary.gross_salary or 0)
        old_deductions = float(salary.total_deductions or 0)
        old_net = float(salary.net_salary or 0)
        old_ctc = float(salary.ctc or 0)

        # Calculate correct gross salary
        gross_salary = (
            float(salary.basic_salary or 0) +
            float(salary.hra or 0) +
            float(salary.conveyance_allowance or 0) +
            float(salary.medical_allowance or 0) +
            float(salary.special_allowance or 0) +
            float(salary.other_allowance or 0)
        )

        # Calculate total deductions
        total_deductions = (
            float(salary.pf_employee or 0) +
            float(salary.esic_employee or 0) +
            float(salary.professional_tax or 0) +
            float(salary.tds or 0)
        )

        # Calculate net salary
        net_salary = gross_salary - total_deductions

        # Calculate CTC
        ctc = gross_salary + float(salary.pf_employer or 0) + float(salary.esic_employer or 0)

        # Check if values changed
        changed = False
        if abs(old_gross - gross_salary) > 0.01:
            print(f"  Gross:      {old_gross:,.2f} -> {gross_salary:,.2f}")
            changed = True

        if abs(old_deductions - total_deductions) > 0.01:
            print(f"  Deductions: {old_deductions:,.2f} -> {total_deductions:,.2f}")
            changed = True

        if abs(old_net - net_salary) > 0.01:
            print(f"  Net:        {old_net:,.2f} -> {net_salary:,.2f}")
            changed = True

        if abs(old_ctc - ctc) > 0.01:
            print(f"  CTC:        {old_ctc:,.2f} -> {ctc:,.2f}")
            print(f"  Annual CTC: {old_ctc * 12:,.2f} -> {ctc * 12:,.2f}")
            changed = True

        if changed:
            salary.gross_salary = gross_salary
            salary.total_deductions = total_deductions
            salary.net_salary = net_salary
            salary.ctc = ctc
            fixed_count += 1
            print("  [UPDATED]")
        else:
            print("  [OK - No changes needed]")

    if fixed_count > 0:
        db.commit()
        print(f"\n{'=' * 80}")
        print(f"[OK] Fixed {fixed_count} salary records")
        print(f"{'=' * 80}")
    else:
        print(f"\n{'=' * 80}")
        print("[OK] All salary records are already correct")
        print(f"{'=' * 80}")

except Exception as e:
    db.rollback()
    print(f"\nError: {e}")
finally:
    db.close()

print("\nDone!")
