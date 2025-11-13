"""Create missing database tables"""
import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll'

from app.db.session import SessionLocal, engine
from app.db.base import Base

# Import all models to ensure they're registered
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.overtime import Overtime
from app.models.advance_loan import Advance, Loan
from app.models.wage import WageStatement

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("[OK] All tables created successfully!")
