"""Add sample holidays for 2025 to employer123 account"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.holiday import Holiday
from datetime import date

def add_sample_holidays():
    db = SessionLocal()

    try:
        # Show all users first
        all_users = db.query(User).all()
        print(f"Found {len(all_users)} users in database:")
        for u in all_users[:5]:  # Show first 5
            print(f"  - {u.username} (role: {u.role}, tenant_id: {u.tenant_id})")

        # Use tenant_id = 1 (the first tenant)
        tenant_id = 1
        print(f"\nUsing tenant_id: {tenant_id}")

        # Sample Indian holidays for 2025
        holidays_2025 = [
            # January
            {"name": "New Year's Day", "date": date(2025, 1, 1), "is_mandatory": True, "description": "New Year celebration"},
            {"name": "Makar Sankranti", "date": date(2025, 1, 14), "is_mandatory": True, "description": "Harvest festival"},
            {"name": "Republic Day", "date": date(2025, 1, 26), "is_mandatory": True, "description": "National holiday"},

            # March
            {"name": "Maha Shivaratri", "date": date(2025, 3, 10), "is_mandatory": True, "description": "Hindu festival"},
            {"name": "Holi", "date": date(2025, 3, 25), "is_mandatory": True, "description": "Festival of colors"},

            # April
            {"name": "Good Friday", "date": date(2025, 4, 18), "is_mandatory": True, "description": "Christian holiday"},
            {"name": "Ram Navami", "date": date(2025, 4, 6), "is_mandatory": False, "description": "Hindu festival"},

            # May
            {"name": "May Day", "date": date(2025, 5, 1), "is_mandatory": False, "description": "Labour Day"},
            {"name": "Buddha Purnima", "date": date(2025, 5, 12), "is_mandatory": False, "description": "Buddha's birthday"},

            # August
            {"name": "Independence Day", "date": date(2025, 8, 15), "is_mandatory": True, "description": "National holiday"},
            {"name": "Raksha Bandhan", "date": date(2025, 8, 9), "is_mandatory": False, "description": "Hindu festival"},
            {"name": "Janmashtami", "date": date(2025, 8, 26), "is_mandatory": True, "description": "Krishna's birthday"},

            # October
            {"name": "Gandhi Jayanti", "date": date(2025, 10, 2), "is_mandatory": True, "description": "Gandhi's birthday"},
            {"name": "Dussehra", "date": date(2025, 10, 22), "is_mandatory": True, "description": "Victory of good over evil"},

            # November
            {"name": "Diwali", "date": date(2025, 11, 1), "is_mandatory": True, "description": "Festival of lights"},
            {"name": "Govardhan Puja", "date": date(2025, 11, 2), "is_mandatory": False, "description": "Hindu festival"},
            {"name": "Bhai Dooj", "date": date(2025, 11, 3), "is_mandatory": False, "description": "Brother-sister festival"},

            # December
            {"name": "Christmas", "date": date(2025, 12, 25), "is_mandatory": True, "description": "Christian holiday"},
        ]

        # Delete existing 2025 holidays for this tenant
        deleted = db.query(Holiday).filter(
            Holiday.tenant_id == tenant_id,
            Holiday.date >= date(2025, 1, 1),
            Holiday.date <= date(2025, 12, 31)
        ).delete()

        print(f"Deleted {deleted} existing 2025 holidays")

        # Add new holidays
        added_count = 0
        for holiday_data in holidays_2025:
            holiday = Holiday(
                tenant_id=tenant_id,
                **holiday_data
            )
            db.add(holiday)
            added_count += 1

        db.commit()
        print(f"Successfully added {added_count} holidays for 2025")

        # Show summary
        mandatory = sum(1 for h in holidays_2025 if h["is_mandatory"])
        optional = len(holidays_2025) - mandatory
        print(f"  - Mandatory holidays: {mandatory}")
        print(f"  - Optional holidays: {optional}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_holidays()
