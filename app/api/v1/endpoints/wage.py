from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.wage import WageStatementResponse
from app.crud.wage import wage as wage_crud
from app.models.user import User
from app.services.wage_template_service import WageTemplateService

router = APIRouter()


@router.get("/template/download")
async def download_template(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Download wage data Excel template
    """
    service = WageTemplateService(db, current_user.tenant_id)
    
    # Get company details (placeholder for now, ideally from tenant settings)
    company_name = "My Company" 
    company_address = "Company Address"
    
    file_path = service.generate_template(company_name, company_address)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail="Failed to generate template")
        
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


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
