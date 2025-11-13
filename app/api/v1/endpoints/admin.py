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
    
    recent_invoices = (
        db.query(BillingInvoice)
        .order_by(BillingInvoice.created_at.desc())
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
            "recent_registrations": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at
                }
                for user in recent_registrations
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

# User management endpoints
@router.get("/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    if not current_user.is_superuser and current_user.role != "saas_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access user management"
        )
    # TODO: Implement user listing
    return {"message": "User management - to be implemented"}

@router.post("/users")
async def create_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    if not current_user.is_superuser and current_user.role != "saas_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users"
        )
    # TODO: Implement user creation
    return {"message": "User creation - to be implemented"}
