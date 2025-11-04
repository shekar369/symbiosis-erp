from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.wage import WageStatement
from app.schemas.wage import WageStatementCreate


class CRUDWage(CRUDBase[WageStatement, WageStatementCreate, dict]):
    def get_wage_statement(self, db: Session, wage_id: int) -> Optional[WageStatement]:
        return db.query(WageStatement).filter(WageStatement.id == wage_id).first()

    def get_wage_statements(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        employee_id: int = None,
        month: int = None,
        year: int = None
    ) -> List[WageStatement]:
        query = db.query(WageStatement)
        if employee_id:
            query = query.filter(WageStatement.employee_id == employee_id)
        if month:
            query = query.filter(WageStatement.month == month)
        if year:
            query = query.filter(WageStatement.year == year)
        return query.offset(skip).limit(limit).all()


wage = CRUDWage(WageStatement)
