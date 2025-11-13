"""Clear failed transaction"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal

db = SessionLocal()

try:
    print("Rolling back any failed transactions...")
    db.rollback()
    print("[OK] Transaction rolled back")

    # Test that we can query now
    print("Testing database connection...")
    result = db.execute("SELECT 1")
    print(f"[OK] Database connection working: {result.scalar()}")

except Exception as e:
    print(f"[ERROR] {e}")
finally:
    db.close()
