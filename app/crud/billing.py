from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.billing import SubscriptionPlan, Subscription, BillingInvoice
from app.schemas.billing import (
    SubscriptionPlanCreate,
    SubscriptionPlanUpdate,
    SubscriptionCreate,
    SubscriptionUpdate,
    BillingInvoiceCreate,
    SubscriptionStatus,
    BillingInterval
)


# Subscription Plan CRUD
def create_subscription_plan(
    db: Session,
    plan_in: SubscriptionPlanCreate
) -> SubscriptionPlan:
    db_plan = SubscriptionPlan(**plan_in.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_subscription_plan(
    db: Session,
    plan_id: int
) -> Optional[SubscriptionPlan]:
    return db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()


def get_active_subscription_plans(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[SubscriptionPlan]:
    return db.query(SubscriptionPlan).filter(
        SubscriptionPlan.is_active == True
    ).offset(skip).limit(limit).all()


def update_subscription_plan(
    db: Session,
    plan: SubscriptionPlan,
    plan_in: SubscriptionPlanUpdate
) -> SubscriptionPlan:
    update_data = plan_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


# Subscription CRUD
def create_subscription(
    db: Session,
    subscription_in: SubscriptionCreate
) -> Subscription:
    # Calculate period dates based on billing interval
    now = datetime.utcnow()
    if subscription_in.billing_interval == BillingInterval.MONTHLY:
        period_end = now + timedelta(days=30)
    elif subscription_in.billing_interval == BillingInterval.QUARTERLY:
        period_end = now + timedelta(days=90)
    else:  # ANNUAL
        period_end = now + timedelta(days=365)

    db_subscription = Subscription(
        **subscription_in.model_dump(),
        current_period_start=now,
        current_period_end=period_end,
        status=SubscriptionStatus.ACTIVE
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def get_subscription(
    db: Session,
    subscription_id: int
) -> Optional[Subscription]:
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()


def get_tenant_subscription(
    db: Session,
    tenant_id: int
) -> Optional[Subscription]:
    return db.query(Subscription).filter(
        Subscription.tenant_id == tenant_id,
        Subscription.status != SubscriptionStatus.CANCELED
    ).first()


def update_subscription(
    db: Session,
    subscription: Subscription,
    subscription_in: SubscriptionUpdate
) -> Subscription:
    update_data = subscription_in.model_dump(exclude_unset=True)
    
    if "status" in update_data and update_data["status"] == SubscriptionStatus.CANCELED:
        subscription.canceled_at = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(subscription, field, value)
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


# Invoice CRUD
def create_invoice(
    db: Session,
    invoice_in: BillingInvoiceCreate
) -> BillingInvoice:
    db_invoice = BillingInvoice(**invoice_in.model_dump())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def get_tenant_invoices(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[BillingInvoice]:
    return db.query(BillingInvoice).filter(
        BillingInvoice.tenant_id == tenant_id
    ).order_by(BillingInvoice.created_at.desc()).offset(skip).limit(limit).all()


def get_unpaid_invoices(
    db: Session,
    tenant_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[BillingInvoice]:
    query = db.query(BillingInvoice).filter(BillingInvoice.status == "unpaid")
    if tenant_id:
        query = query.filter(BillingInvoice.tenant_id == tenant_id)
    return query.order_by(BillingInvoice.due_date.asc()).offset(skip).limit(limit).all()


def mark_invoice_paid(
    db: Session,
    invoice: BillingInvoice,
    payment_reference: str
) -> BillingInvoice:
    invoice.status = "paid"
    invoice.paid_at = datetime.utcnow()
    invoice.payment_reference = payment_reference
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice