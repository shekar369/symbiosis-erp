from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db, get_saas_admin, get_employer_admin,
    get_employee, get_auditor
)
from app.models.user import User

router = APIRouter()

@router.get("/saas-admin/dashboard")
async def saas_admin_dashboard(
    current_user: User = Depends(get_saas_admin),
    db: Session = Depends(get_db)
):
    """
    Get SaaS Admin dashboard with system-wide statistics and monitoring data
    """
    from app.models.registration import OrganizationRegistration
    from app.schemas.registration import RegistrationStatus
    
    # Get tenant statistics
    total_tenants = db.query(User).filter(User.role == "employer_admin").count()
    active_tenants = db.query(User).filter(
        User.role == "employer_admin",
        User.is_active == True
    ).count()
    
    # Get user statistics
    total_users = db.query(User).count()
    user_by_role = {
        "employer_admin": db.query(User).filter(User.role == "employer_admin").count(),
        "employee": db.query(User).filter(User.role == "employee").count(),
        "auditor": db.query(User).filter(User.role == "auditor").count()
    }
    
    from app.models.billing import Subscription, BillingInvoice, SubscriptionStatus
    
    # Get registration statistics
    registration_stats = {
        "pending": db.query(OrganizationRegistration)
            .filter(OrganizationRegistration.status == RegistrationStatus.PENDING).count(),
        "approved": db.query(OrganizationRegistration)
            .filter(OrganizationRegistration.status == RegistrationStatus.APPROVED).count(),
        "rejected": db.query(OrganizationRegistration)
            .filter(OrganizationRegistration.status == RegistrationStatus.REJECTED).count()
    }
    
    # Get subscription statistics
    subscription_stats = {
        "active": db.query(Subscription)
            .filter(Subscription.status == SubscriptionStatus.ACTIVE).count(),
        "trial": db.query(Subscription)
            .filter(Subscription.status == SubscriptionStatus.TRIAL).count(),
        "past_due": db.query(Subscription)
            .filter(Subscription.status == SubscriptionStatus.PAST_DUE).count(),
        "canceled": db.query(Subscription)
            .filter(Subscription.status == SubscriptionStatus.CANCELED).count()
    }
    
    # Get billing statistics
    total_invoiced = db.query(func.sum(BillingInvoice.amount)).scalar() or 0
    total_paid = db.query(func.sum(BillingInvoice.amount))\
        .filter(BillingInvoice.status == "paid").scalar() or 0
    total_unpaid = db.query(func.sum(BillingInvoice.amount))\
        .filter(BillingInvoice.status == "unpaid").scalar() or 0
    
    billing_stats = {
        "total_invoiced": float(total_invoiced),
        "total_paid": float(total_paid),
        "total_unpaid": float(total_unpaid),
        "unpaid_invoices": db.query(BillingInvoice)
            .filter(BillingInvoice.status == "unpaid").count()
    }
    
    # Get recent activities
    recent_registrations = (
        db.query(OrganizationRegistration)
        .order_by(OrganizationRegistration.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "dashboard_data": {
            "tenant_stats": {
                "total": total_tenants,
                "active": active_tenants,
                "inactive": total_tenants - active_tenants
            },
            "user_stats": {
                "total_users": total_users,
                "by_role": user_by_role
            },
            "registration_stats": registration_stats,
            "recent_registrations": [
                {
                    "id": reg.id,
                    "name": reg.name,
                    "email": reg.email,
                    "contact_person": reg.contact_person,
                    "status": reg.status,
                    "created_at": str(reg.created_at)
                }
                for reg in recent_registrations
            ]
        },
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role
        }
    }
@router.get("/employer/dashboard")
async def employer_dashboard(
    current_user: User = Depends(get_employer_admin),
    db: Session = Depends(get_db)
):
    return {
        "message": "Employer Dashboard",
        "user": current_user.username,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id
    }

@router.get("/employee/dashboard")
async def employee_dashboard(
    current_user: User = Depends(get_employee),
    db: Session = Depends(get_db)
):
    return {
        "message": "Employee Dashboard",
        "user": current_user.username,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id
    }

@router.get("/auditor/dashboard")
async def auditor_dashboard(
    current_user: User = Depends(get_auditor),
    db: Session = Depends(get_db)
):
    return {
        "message": "Auditor Dashboard",
        "user": current_user.username,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id
    }

from pydantic import BaseModel as _BaseModel


class UserCreateRequest(_BaseModel):
    username: str
    email: str
    password: str
    role: str
    full_name: str = None
    tenant_id: int = None


@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    role: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin),
):
    """List all users across all tenants (SaaS admin only)."""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    total = db.query(User).count()
    return {
        "total": total,
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "full_name": u.full_name,
                "is_active": u.is_active,
                "tenant_id": u.tenant_id,
                "created_at": str(u.created_at),
            }
            for u in users
        ],
    }


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin),
):
    """Create a new user (SaaS admin only)."""
    from app.crud.user import user as user_crud
    from app.core.security import get_password_hash

    if user_crud.get_user_by_username(db, payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    if user_crud.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    valid_roles = ["saas_admin", "employer_admin", "employee", "auditor"]
    if payload.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid role. Must be one of: {valid_roles}",
        )

    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
        full_name=payload.full_name,
        tenant_id=payload.tenant_id,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "tenant_id": new_user.tenant_id,
    }
