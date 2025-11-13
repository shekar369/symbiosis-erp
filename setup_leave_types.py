"""
Setup default leave types for the HR Payroll system
"""
import os
import sys

# Ensure DATABASE_URL is not set in environment
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.leave import LeaveType
from app.models.tenant import Tenant

def setup_leave_types():
    db: Session = SessionLocal()

    try:
        print("=" * 70)
        print("SETTING UP DEFAULT LEAVE TYPES")
        print("=" * 70)

        # Get all tenants
        tenants = db.query(Tenant).all()

        if not tenants:
            print("\n[ERROR] No tenants found. Please create a tenant first.")
            return False

        # Default leave types for Indian companies
        # Note: LeaveType model only has: tenant_id, name, code, days_per_year, is_paid
        default_leave_types = [
            {
                "name": "Casual Leave",
                "code": "CL",
                "days_per_year": 12,
                "is_paid": 1
            },
            {
                "name": "Sick Leave",
                "code": "SL",
                "days_per_year": 12,
                "is_paid": 1
            },
            {
                "name": "Privilege Leave",
                "code": "PL",
                "days_per_year": 21,
                "is_paid": 1
            },
            {
                "name": "Maternity Leave",
                "code": "ML",
                "days_per_year": 182,  # 26 weeks
                "is_paid": 1
            },
            {
                "name": "Paternity Leave",
                "code": "PTL",
                "days_per_year": 15,
                "is_paid": 1
            },
            {
                "name": "Compensatory Off",
                "code": "CO",
                "days_per_year": 12,
                "is_paid": 1
            },
            {
                "name": "Loss of Pay",
                "code": "LOP",
                "days_per_year": 365,
                "is_paid": 0  # Unpaid leave
            }
        ]

        created_count = 0
        exists_count = 0

        for tenant in tenants:
            print(f"\n\nTenant: {tenant.name} (ID: {tenant.id})")
            print("-" * 70)

            for leave_type_data in default_leave_types:
                # Make code unique per tenant by prefixing with tenant ID
                unique_code = f"T{tenant.id}-{leave_type_data['code']}"

                # Check if leave type already exists for this tenant
                existing = db.query(LeaveType).filter(
                    LeaveType.tenant_id == tenant.id,
                    LeaveType.code == unique_code
                ).first()

                if existing:
                    print(f"  [EXISTS] {leave_type_data['name']} ({leave_type_data['code']})")
                    exists_count += 1
                else:
                    leave_type = LeaveType(
                        tenant_id=tenant.id,
                        name=leave_type_data["name"],
                        code=unique_code,
                        days_per_year=leave_type_data["days_per_year"],
                        is_paid=leave_type_data["is_paid"]
                    )
                    db.add(leave_type)
                    print(f"  [CREATED] {leave_type_data['name']} ({leave_type_data['code']}) - {leave_type_data['days_per_year']} days/year")
                    created_count += 1

            db.commit()

        print("\n" + "=" * 70)
        print("LEAVE TYPES SETUP COMPLETE!")
        print("=" * 70)
        print(f"\nTotal Tenants: {len(tenants)}")
        print(f"Leave Types Created: {created_count}")
        print(f"Leave Types Already Existed: {exists_count}")
        print(f"\nLeave types are now available for employees to apply!")
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
    success = setup_leave_types()
    if success:
        print("\n[SUCCESS] Leave types setup completed!")
    else:
        print("\n[FAILED] Failed to setup leave types.")
        sys.exit(1)
