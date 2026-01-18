"""Reset all user passwords to standard test passwords"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_passwords():
    db = SessionLocal()

    try:
        print("=" * 80)
        print("RESETTING USER PASSWORDS")
        print("=" * 80)
        print()

        # Define password mappings
        password_mappings = {
            "admin": "admin123",
            "employer": "employer123",
            "hrmanager": "hr_manager123",
            "employee": "employee123"
        }

        users = db.query(User).all()
        reset_count = 0

        for user in users:
            if user.username in password_mappings:
                new_password = password_mappings[user.username]
                user.hashed_password = get_password_hash(new_password)
                reset_count += 1

                print(f"Reset password for: {user.username}")
                print(f"  Email: {user.email}")
                print(f"  Role: {user.role}")
                print(f"  New Password: {new_password}")
                print(f"  Tenant ID: {user.tenant_id}")
                print()

        # Commit changes
        db.commit()

        print("=" * 80)
        print(f"Successfully reset {reset_count} passwords!")
        print("=" * 80)
        print()

        print("UPDATED CREDENTIALS:")
        print("-" * 80)
        for user in users:
            if user.username in password_mappings:
                print(f"Username: {user.username:12} | Password: {password_mappings[user.username]:15} | Role: {user.role}")

        print()
        print("=" * 80)
        print("Password reset complete! Please test login now.")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_passwords()
