from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import date, datetime, time
from typing import List, Optional

from app.models.attendance import Attendance, AttendanceStatus


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    def mark_attendance(
        self,
        employee_id: int,
        attendance_date: date,
        check_in: Optional[time],
        check_out: Optional[time],
    ) -> Attendance:
        """Create or update a single attendance record for the given date."""
        hours = self.calculate_hours_worked(check_in, check_out)
        status = AttendanceStatus.PRESENT if check_in else AttendanceStatus.ABSENT

        existing = (
            self.db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.date == attendance_date,
            )
            .first()
        )
        if existing:
            existing.check_in = check_in
            existing.check_out = check_out
            existing.hours_worked = hours
            existing.status = status
            self.db.commit()
            self.db.refresh(existing)
            return existing

        record = Attendance(
            employee_id=employee_id,
            date=attendance_date,
            check_in=check_in,
            check_out=check_out,
            hours_worked=hours,
            status=status,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def process_attendance_upload(self, file_path: str, tenant_id: int) -> dict:
        """Delegate bulk Excel/CSV processing to the dedicated upload service."""
        from app.services.attendance_upload_service import AttendanceUploadService
        service = AttendanceUploadService(self.db)
        return service.process_file(file_path, tenant_id)

    def calculate_hours_worked(
        self, check_in: Optional[time], check_out: Optional[time]
    ) -> float:
        """Return hours between check-in and check-out, or 0 if either is missing."""
        if not check_in or not check_out:
            return 0.0
        today = date.today()
        ci = datetime.combine(today, check_in)
        co = datetime.combine(today, check_out)
        if co <= ci:
            return 0.0
        return round((co - ci).total_seconds() / 3600, 2)

    def get_monthly_attendance(
        self, employee_id: int, month: int, year: int
    ) -> List[Attendance]:
        """Return all attendance records for an employee in a given month."""
        return (
            self.db.query(Attendance)
            .filter(
                and_(
                    Attendance.employee_id == employee_id,
                    extract("month", Attendance.date) == month,
                    extract("year", Attendance.date) == year,
                )
            )
            .order_by(Attendance.date)
            .all()
        )
