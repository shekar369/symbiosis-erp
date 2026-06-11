from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional

from app.models.leave import LeaveRequest, LeaveBalance, LeaveStatus
from app.crud.leave import leave_request as leave_crud


class LeaveService:
    def __init__(self, db: Session):
        self.db = db

    def apply_leave(
        self,
        employee_id: int,
        leave_type_id: int,
        start_date: date,
        end_date: date,
        reason: str,
    ) -> LeaveRequest:
        """Create a leave request after validating available balance."""
        days = self.calculate_leave_days(start_date, end_date)

        balance = (
            self.db.query(LeaveBalance)
            .filter(
                LeaveBalance.employee_id == employee_id,
                LeaveBalance.leave_type_id == leave_type_id,
            )
            .first()
        )
        if balance and balance.balance_days < days:
            raise ValueError(
                f"Insufficient leave balance. Available: {balance.balance_days:.1f}, "
                f"Requested: {days:.1f}"
            )

        request = LeaveRequest(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            start_date=start_date,
            end_date=end_date,
            days=days,
            reason=reason,
            status=LeaveStatus.PENDING,
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def approve_leave(self, leave_request_id: int, approved_by: int) -> Optional[LeaveRequest]:
        result = leave_crud.approve_request(self.db, leave_request_id, approved_by)
        if result:
            self.update_leave_balance(result.employee_id, result.leave_type_id, result.days)
        return result

    def reject_leave(self, leave_request_id: int, approved_by: int) -> Optional[LeaveRequest]:
        return leave_crud.reject_request(self.db, leave_request_id, approved_by, "Rejected")

    def calculate_leave_days(self, start_date: date, end_date: date) -> float:
        """Count business days (Mon–Fri) between start_date and end_date inclusive."""
        days = 0.0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:
                days += 1
            current += timedelta(days=1)
        return days

    def update_leave_balance(
        self, employee_id: int, leave_type_id: int, days: float
    ) -> None:
        """Deduct approved leave days from the employee's running balance."""
        balance = (
            self.db.query(LeaveBalance)
            .filter(
                LeaveBalance.employee_id == employee_id,
                LeaveBalance.leave_type_id == leave_type_id,
            )
            .first()
        )
        if balance:
            balance.used_days += days
            balance.balance_days = balance.total_days - balance.used_days
            self.db.commit()
