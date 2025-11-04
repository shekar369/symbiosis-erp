from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_employee(self, db: Session, employee_id: int) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.id == employee_id).first()

    def get_employees(self, db: Session, skip: int = 0, limit: int = 20) -> List[Employee]:
        return db.query(Employee).offset(skip).limit(limit).all()

    def create_employee(self, db: Session, employee: EmployeeCreate) -> Employee:
        return self.create(db, obj_in=employee)

    def update_employee(self, db: Session, employee_id: int, employee_update: EmployeeUpdate) -> Optional[Employee]:
        db_employee = self.get_employee(db, employee_id)
        if db_employee:
            return self.update(db, db_obj=db_employee, obj_in=employee_update)
        return None

    def delete_employee(self, db: Session, employee_id: int) -> bool:
        db_employee = self.get_employee(db, employee_id)
        if db_employee:
            self.remove(db, id=employee_id)
            return True
        return False


employee = CRUDEmployee(Employee)
