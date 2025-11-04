from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_saas_admin
from app.models.user import User
from app.crud import billing as billing_crud
from app.schemas.billing import (
    SubscriptionPlanCreate,
    SubscriptionPlanUpdate,
    SubscriptionPlanResponse,
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse,
    BillingInvoiceCreate,
    BillingInvoiceResponse
)

router = APIRouter()

# Subscription Plans endpoints
@router.post("/plans", response_model=SubscriptionPlanResponse)
async def create_subscription_plan(
    plan: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Create a new subscription plan (SaaS Admin only)"""
    return billing_crud.create_subscription_plan(db, plan)

@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def list_subscription_plans(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List all active subscription plans"""
    return billing_crud.get_active_subscription_plans(db, skip=skip, limit=limit)

@router.put("/plans/{plan_id}", response_model=SubscriptionPlanResponse)
async def update_subscription_plan(
    plan_id: int,
    plan_update: SubscriptionPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Update a subscription plan (SaaS Admin only)"""
    plan = billing_crud.get_subscription_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    return billing_crud.update_subscription_plan(db, plan, plan_update)

# Subscriptions endpoints
@router.post("/subscriptions", response_model=SubscriptionResponse)
async def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Create a new subscription for a tenant (SaaS Admin only)"""
    existing = billing_crud.get_tenant_subscription(db, subscription.tenant_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Tenant already has an active subscription"
        )
    return billing_crud.create_subscription(db, subscription)

@router.get("/subscriptions/tenant/{tenant_id}", response_model=SubscriptionResponse)
async def get_tenant_subscription(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Get a tenant's active subscription"""
    subscription = billing_crud.get_tenant_subscription(db, tenant_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return subscription

@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Update a subscription (SaaS Admin only)"""
    subscription = billing_crud.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return billing_crud.update_subscription(db, subscription, subscription_update)

# Invoices endpoints
@router.post("/invoices", response_model=BillingInvoiceResponse)
async def create_invoice(
    invoice: BillingInvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Create a new invoice (SaaS Admin only)"""
    return billing_crud.create_invoice(db, invoice)

@router.get("/invoices/tenant/{tenant_id}", response_model=List[BillingInvoiceResponse])
async def list_tenant_invoices(
    tenant_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List all invoices for a tenant"""
    return billing_crud.get_tenant_invoices(db, tenant_id, skip=skip, limit=limit)

@router.get("/invoices/unpaid", response_model=List[BillingInvoiceResponse])
async def list_unpaid_invoices(
    tenant_id: int = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List all unpaid invoices"""
    return billing_crud.get_unpaid_invoices(db, tenant_id, skip=skip, limit=limit)

@router.post("/invoices/{invoice_id}/mark-paid", response_model=BillingInvoiceResponse)
async def mark_invoice_paid(
    invoice_id: int,
    payment_reference: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Mark an invoice as paid (SaaS Admin only)"""
    invoice = billing_crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return billing_crud.mark_invoice_paid(db, invoice, payment_reference)