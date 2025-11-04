from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class CRUDAttendance(CRUDBase[Attendance, AttendanceCreate, AttendanceUpdate]):
    def get_attendance_records(
        self, db: Session, skip: int = 0, limit: int = 20, employee_id: int = None
    ) -> List[Attendance]:
        query = db.query(Attendance)
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        return query.offset(skip).limit(limit).all()

    def create_attendance(self, db: Session, attendance: AttendanceCreate) -> Attendance:
        return self.create(db, obj_in=attendance)


attendance = CRUDAttendance(Attendance)
