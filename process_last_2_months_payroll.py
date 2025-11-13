"""Process payroll for all employees for the last 2 months"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal
from app.services.wage_calculation_service import WageCalculationService

db = SessionLocal()

try:
    print("=" * 80)
    print("PROCESSING PAYROLL FOR LAST 2 MONTHS (SEPTEMBER & OCTOBER 2025)")
    print("=" * 80)

    service = WageCalculationService(db)

    # Process September 2025
    print("\n\nPROCESSING SEPTEMBER 2025...")
    print("-" * 80)
    result_sep = service.process_bulk_payroll(
        tenant_id=1,
        month=9,
        year=2025
    )

    print(f"\nSeptember 2025 Results:")
    print(f"  Total Employees: {result_sep['total_employees']}")
    print(f"  Successful: {result_sep['successful']}")
    print(f"  Failed: {result_sep['failed']}")

    if result_sep['successful_records']:
        print(f"\n  Successful Employees:")
        for record in result_sep['successful_records']:
            print(f"    - {record['employee_code']}: Rs.{record['net_salary']:,.2f}")

    if result_sep['failed_records']:
        print(f"\n  Failed Employees:")
        for record in result_sep['failed_records']:
            print(f"    - {record['employee_code']}: {record['error']}")

    # Process October 2025
    print("\n\nPROCESSING OCTOBER 2025...")
    print("-" * 80)
    result_oct = service.process_bulk_payroll(
        tenant_id=1,
        month=10,
        year=2025
    )

    print(f"\nOctober 2025 Results:")
    print(f"  Total Employees: {result_oct['total_employees']}")
    print(f"  Successful: {result_oct['successful']}")
    print(f"  Failed: {result_oct['failed']}")

    if result_oct['successful_records']:
        print(f"\n  Successful Employees:")
        for record in result_oct['successful_records']:
            print(f"    - {record['employee_code']}: Rs.{record['net_salary']:,.2f}")

    if result_oct['failed_records']:
        print(f"\n  Failed Employees:")
        for record in result_oct['failed_records']:
            print(f"    - {record['employee_code']}: {record['error']}")

    print("\n" + "=" * 80)
    print("[SUCCESS] Payroll processing completed!")
    print("=" * 80)
    print(f"\nTotal Summary:")
    print(f"  September: {result_sep['successful']}/{result_sep['total_employees']} successful")
    print(f"  October: {result_oct['successful']}/{result_oct['total_employees']} successful")
    print(f"  Overall: {result_sep['successful'] + result_oct['successful']}/{result_sep['total_employees'] + result_oct['total_employees']} successful")

except Exception as e:
    print("\n[ERROR] Payroll processing failed!")
    print("=" * 80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
