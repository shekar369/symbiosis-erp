from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.wage import WageStatementResponse
from app.crud.wage import wage as wage_crud
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[WageStatementResponse])
async def list_wage_statements(
    skip: int = 0,
    limit: int = 20,
    employee_id: int = None,
    month: int = None,
    year: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return wage_crud.get_wage_statements(
        db=db, skip=skip, limit=limit, employee_id=employee_id, month=month, year=year
    )


@router.get("/{wage_id}", response_model=WageStatementResponse)
async def get_wage_statement(
    wage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    wage = wage_crud.get_wage_statement(db=db, wage_id=wage_id)
    if not wage:
        raise HTTPException(status_code=404, detail="Wage statement not found")
    return wage
