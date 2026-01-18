"""Validate all user credentials by attempting login"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password
from passlib.context import CryptContext

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Common test passwords to try
TEST_PASSWORDS = [
    "admin123",
    "employer123",
    "hr123",
    "hr_manager123",
    "hrmanager123",
    "employee123",
    "password123",
    "test123"
]

def validate_credentials():
    db = SessionLocal()

    try:
        print("=" * 80)
        print("CREDENTIAL VALIDATION REPORT")
        print("=" * 80)
        print()

        users = db.query(User).order_by(User.tenant_id, User.role, User.id).all()

        print(f"Total users found: {len(users)}\n")

        validated_credentials = []

        for user in users:
            print(f"\nValidating: {user.username} ({user.role})")
            print(f"  Email: {user.email}")
            print(f"  Full Name: {user.full_name}")
            print(f"  Tenant ID: {user.tenant_id}")
            print(f"  Active: {user.is_active}")
            print(f"  Hashed Password: {user.hashed_password[:50]}...")

            # Try to validate with common passwords
            password_found = None
            for test_pwd in TEST_PASSWORDS:
                try:
                    if pwd_context.verify(test_pwd, user.hashed_password):
                        password_found = test_pwd
                        print(f"  ✅ PASSWORD VALIDATED: {test_pwd}")
                        break
                except Exception as e:
                    pass

            if not password_found:
                print(f"  ❌ Password NOT found in test list")
                print(f"     (Try resetting password or checking database)")

            validated_credentials.append({
                "username": user.username,
                "password": password_found if password_found else "UNKNOWN",
                "email": user.email,
                "role": user.role,
                "full_name": user.full_name,
                "tenant_id": user.tenant_id,
                "is_active": user.is_active,
                "validated": password_found is not None
            })

        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print()

        for cred in validated_credentials:
            status = "✅ VALID" if cred["validated"] else "❌ INVALID"
            print(f"{status} | Username: {cred['username']:15} | Password: {cred['password']:20} | Role: {cred['role']:15}")

        print("\n" + "=" * 80)
        print("VERIFIED CREDENTIALS TABLE")
        print("=" * 80)
        print()
        print("| Username | Password | Role | Tenant ID | Full Name | Status |")
        print("|----------|----------|------|-----------|-----------|--------|")

        for cred in validated_credentials:
            status = "✅" if cred["validated"] else "❌"
            print(f"| {cred['username']} | {cred['password']} | {cred['role']} | {cred['tenant_id']} | {cred['full_name']} | {status} |")

        print()
        print("=" * 80)

        # Count valid vs invalid
        valid_count = sum(1 for c in validated_credentials if c["validated"])
        invalid_count = len(validated_credentials) - valid_count

        print(f"✅ Valid credentials: {valid_count}/{len(validated_credentials)}")
        print(f"❌ Invalid credentials: {invalid_count}/{len(validated_credentials)}")
        print("=" * 80)

        return validated_credentials

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        db.close()

if __name__ == "__main__":
    validate_credentials()
