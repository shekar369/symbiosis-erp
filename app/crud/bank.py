from sqlalchemy.orm import Session
from typing import Optional

from app.models.employee import EmployeeBankDetails
from app.schemas.bank import BankDetailsCreate, BankDetailsUpdate


class CRUDBankDetails:
    def get_by_employee(self, db: Session, employee_id: int) -> Optional[EmployeeBankDetails]:
        """Get bank details for a specific employee"""
        return db.query(EmployeeBankDetails).filter(
            EmployeeBankDetails.employee_id == employee_id
        ).first()

    def create(self, db: Session, bank_details: BankDetailsCreate) -> EmployeeBankDetails:
        """Create new bank details for an employee"""
        db_bank_details = EmployeeBankDetails(**bank_details.model_dump())
        db.add(db_bank_details)
        db.commit()
        db.refresh(db_bank_details)
        return db_bank_details

    def update(
        self,
        db: Session,
        employee_id: int,
        bank_update: BankDetailsUpdate
    ) -> Optional[EmployeeBankDetails]:
        """Update bank details for an employee"""
        db_bank_details = self.get_by_employee(db=db, employee_id=employee_id)
        if not db_bank_details:
            return None

        update_data = bank_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bank_details, field, value)

        db.commit()
        db.refresh(db_bank_details)
        return db_bank_details

    def delete(self, db: Session, employee_id: int) -> bool:
        """Delete bank details for an employee"""
        db_bank_details = self.get_by_employee(db=db, employee_id=employee_id)
        if not db_bank_details:
            return False

        db.delete(db_bank_details)
        db.commit()
        return True


bank_details = CRUDBankDetails()
