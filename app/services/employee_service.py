from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.models.employee import Employee, EmployeeStatus
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud.employee import employee as employee_crud


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        return employee_crud.create_employee(self.db, employee_data)

    def update_employee(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
        return employee_crud.update_employee(self.db, employee_id, employee_data)

    def get_employee_details(self, employee_id: int) -> Optional[Employee]:
        return employee_crud.get_employee(self.db, employee_id)

    def terminate_employee(self, employee_id: int, termination_date: date) -> bool:
        """Set employee status to TERMINATED and record the leaving date."""
        emp = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not emp:
            return False
        emp.status = EmployeeStatus.TERMINATED.value
        emp.date_of_leaving = termination_date
        self.db.commit()
        return True

    def get_employees_by_tenant(
        self, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> List[Employee]:
        return (
            self.db.query(Employee)
            .filter(Employee.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
