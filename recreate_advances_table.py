"""Drop and recreate advances table with new schema"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal, engine
from app.models.advance_loan import Advance

print("Dropping advances table...")
Advance.__table__.drop(engine, checkfirst=True)
print("[OK] advances table dropped")

print("Creating advances table with new schema...")
Advance.__table__.create(engine)
print("[OK] advances table created")

print("\nTable schema:")
print(f"  Columns: {[c.name for c in Advance.__table__.columns]}")
