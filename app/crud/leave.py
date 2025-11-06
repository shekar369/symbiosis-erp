from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from app.crud.base import CRUDBase
from app.models.leave import LeaveRequest, LeaveBalance, LeaveType
from app.schemas.leave import LeaveRequestCreate, LeaveRequestUpdate, LeaveTypeCreate, LeaveTypeUpdate


class CRUDLeaveRequest(CRUDBase[LeaveRequest, LeaveRequestCreate, LeaveRequestUpdate]):
    def get_by_employee(
        self, db: Session, employee_id: int, skip: int = 0, limit: int = 20
    ) -> List[LeaveRequest]:
        return (
            db.query(LeaveRequest)
            .filter(LeaveRequest.employee_id == employee_id)
            .order_by(LeaveRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending_requests(
        self, db: Session, skip: int = 0, limit: int = 20
    ) -> List[LeaveRequest]:
        return (
            db.query(LeaveRequest)
            .filter(LeaveRequest.status == "PENDING")
            .order_by(LeaveRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def approve_request(
        self, db: Session, request_id: int, approved_by: int, remarks: str = None
    ) -> Optional[LeaveRequest]:
        leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
        if leave_request and leave_request.status == "PENDING":
            leave_request.status = "APPROVED"
            leave_request.approved_by = approved_by
            leave_request.approved_date = date.today()
            if remarks:
                leave_request.remarks = remarks

            # Deduct from leave balance
            self._update_leave_balance(db, leave_request.employee_id, leave_request.leave_type_id, leave_request.days)

            db.commit()
            db.refresh(leave_request)
            return leave_request
        return None

    def reject_request(
        self, db: Session, request_id: int, rejected_by: int, remarks: str
    ) -> Optional[LeaveRequest]:
        leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
        if leave_request and leave_request.status == "PENDING":
            leave_request.status = "REJECTED"
            leave_request.approved_by = rejected_by
            leave_request.approved_date = date.today()
            leave_request.remarks = remarks
            db.commit()
            db.refresh(leave_request)
            return leave_request
        return None

    def cancel_request(
        self, db: Session, request_id: int, employee_id: int
    ) -> Optional[LeaveRequest]:
        leave_request = db.query(LeaveRequest).filter(
            LeaveRequest.id == request_id,
            LeaveRequest.employee_id == employee_id
        ).first()
        if leave_request and leave_request.status in ["PENDING", "APPROVED"]:
            if leave_request.status == "APPROVED":
                # Restore leave balance
                self._update_leave_balance(db, leave_request.employee_id, leave_request.leave_type_id, -leave_request.days)

            leave_request.status = "CANCELLED"
            db.commit()
            db.refresh(leave_request)
            return leave_request
        return None

    def _update_leave_balance(
        self, db: Session, employee_id: int, leave_type_id: int, days: float
    ):
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type_id == leave_type_id
        ).first()

        if balance:
            balance.balance_days -= days
            balance.used_days += days
            db.commit()


class CRUDLeaveBalance(CRUDBase[LeaveBalance, dict, dict]):
    def get_by_employee(
        self, db: Session, employee_id: int
    ) -> List[LeaveBalance]:
        return db.query(LeaveBalance).filter(LeaveBalance.employee_id == employee_id).all()

    def get_balance(
        self, db: Session, employee_id: int, leave_type_id: int
    ) -> Optional[LeaveBalance]:
        return db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type_id == leave_type_id
        ).first()

    def initialize_balance(
        self, db: Session, employee_id: int, leave_type_id: int, allocated_days: float
    ) -> LeaveBalance:
        balance = LeaveBalance(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            allocated_days=allocated_days,
            used_days=0,
            balance_days=allocated_days
        )
        db.add(balance)
        db.commit()
        db.refresh(balance)
        return balance


class CRUDLeaveType(CRUDBase[LeaveType, LeaveTypeCreate, LeaveTypeUpdate]):
    def get_active(self, db: Session, tenant_id: int) -> List[LeaveType]:
        return db.query(LeaveType).filter(
            LeaveType.tenant_id == tenant_id,
            LeaveType.is_active == True
        ).all()

    def get_all(self, db: Session, tenant_id: int) -> List[LeaveType]:
        return db.query(LeaveType).filter(LeaveType.tenant_id == tenant_id).all()

    def get_by_id(self, db: Session, leave_type_id: int, tenant_id: int) -> Optional[LeaveType]:
        return db.query(LeaveType).filter(
            LeaveType.id == leave_type_id,
            LeaveType.tenant_id == tenant_id
        ).first()

    def get_by_code(self, db: Session, code: str, tenant_id: int) -> Optional[LeaveType]:
        return db.query(LeaveType).filter(
            LeaveType.code == code,
            LeaveType.tenant_id == tenant_id
        ).first()

    def create(self, db: Session, leave_type: LeaveTypeCreate, tenant_id: int) -> LeaveType:
        db_leave_type = LeaveType(
            tenant_id=tenant_id,
            name=leave_type.name,
            code=leave_type.code,
            days_per_year=leave_type.days_per_year,
            is_paid=leave_type.is_paid,
            carry_forward=leave_type.carry_forward,
            max_carry_forward_days=leave_type.max_carry_forward_days,
            description=leave_type.description
        )
        db.add(db_leave_type)
        db.commit()
        db.refresh(db_leave_type)
        return db_leave_type

    def update(self, db: Session, leave_type_id: int, leave_type_update: LeaveTypeUpdate, tenant_id: int) -> Optional[LeaveType]:
        db_leave_type = self.get_by_id(db, leave_type_id, tenant_id)
        if not db_leave_type:
            return None

        update_data = leave_type_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_leave_type, field, value)

        db.commit()
        db.refresh(db_leave_type)
        return db_leave_type

    def delete(self, db: Session, leave_type_id: int, tenant_id: int) -> bool:
        db_leave_type = self.get_by_id(db, leave_type_id, tenant_id)
        if not db_leave_type:
            return False

        # Soft delete - set is_active to False
        db_leave_type.is_active = False
        db.commit()
        return True


leave_request = CRUDLeaveRequest(LeaveRequest)
leave_balance = CRUDLeaveBalance(LeaveBalance)
leave_type = CRUDLeaveType(LeaveType)
