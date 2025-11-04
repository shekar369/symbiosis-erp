from sqlalchemy.orm import Session
from datetime import date

from app.models.leave import LeaveRequest


class LeaveService:
    def __init__(self, db: Session):
        self.db = db

    def apply_leave(self, employee_id: int, leave_type_id: int, start_date: date, end_date: date, reason: str):
        # TODO: Implement leave application logic
        pass

    def approve_leave(self, leave_request_id: int, approved_by: int):
        # TODO: Implement leave approval
        pass

    def reject_leave(self, leave_request_id: int, approved_by: int):
        # TODO: Implement leave rejection
        pass

    def calculate_leave_days(self, start_date: date, end_date: date) -> float:
        # TODO: Calculate number of leave days excluding weekends/holidays
        pass

    def update_leave_balance(self, employee_id: int, leave_type_id: int, days: float):
        # TODO: Update leave balance after approval
        pass
