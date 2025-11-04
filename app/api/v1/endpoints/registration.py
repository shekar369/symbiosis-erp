from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_saas_admin
from app.models.user import User
from app.crud import registration as registration_crud
from app.schemas.registration import (
    OrganizationRegistrationCreate,
    OrganizationRegistrationUpdate,
    OrganizationRegistrationResponse,
    RegistrationStatus
)

router = APIRouter()

@router.post("/register", response_model=OrganizationRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_organization(
    registration: OrganizationRegistrationCreate,
    db: Session = Depends(get_db)
):
    """Public endpoint for organization registration"""
    # Check if organization with same email already registered
    if registration_crud.get_registration_by_email(db, registration.email):
        raise HTTPException(
            status_code=400,
            detail="Organization with this email already registered"
        )
    return registration_crud.create_registration(db, registration)

@router.get("/registrations", response_model=List[OrganizationRegistrationResponse])
async def list_registrations(
    status: RegistrationStatus = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List all organization registrations (SaaS Admin only)"""
    return registration_crud.get_registrations(db, skip=skip, limit=limit, status=status)

@router.get("/registrations/pending", response_model=List[OrganizationRegistrationResponse])
async def list_pending_registrations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List pending organization registrations (SaaS Admin only)"""
    return registration_crud.get_pending_registrations(db, skip=skip, limit=limit)

@router.get("/registrations/stats")
async def get_registration_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Get registration statistics by status (SaaS Admin only)"""
    return {
        "counts": registration_crud.get_registration_count_by_status(db)
    }

@router.get("/registrations/{registration_id}", response_model=OrganizationRegistrationResponse)
async def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Get specific registration details (SaaS Admin only)"""
    registration = registration_crud.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration

@router.put("/registrations/{registration_id}/review", response_model=OrganizationRegistrationResponse)
async def review_registration(
    registration_id: int,
    review: OrganizationRegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Review and update registration status (SaaS Admin only)"""
    registration = registration_crud.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    if registration.status != RegistrationStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Registration already {registration.status}")
    
    return registration_crud.update_registration_status(
        db, 
        registration=registration,
        update_data=review,
        reviewer_id=current_user.id
    )