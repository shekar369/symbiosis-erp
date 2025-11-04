from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, condecimal
from decimal import Decimal


class BillingInterval(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    EXPIRED = "expired"
    TRIAL = "trial"


class PlanFeature(BaseModel):
    name: str
    value: str
    description: Optional[str] = None


class SubscriptionPlanBase(BaseModel):
    name: str
    description: str
    price_monthly: condecimal(max_digits=10, decimal_places=2)
    price_quarterly: condecimal(max_digits=10, decimal_places=2)
    price_annual: condecimal(max_digits=10, decimal_places=2)
    max_employees: int
    features: List[PlanFeature]
    is_active: bool = True


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[Decimal] = None
    price_quarterly: Optional[Decimal] = None
    price_annual: Optional[Decimal] = None
    max_employees: Optional[int] = None
    features: Optional[List[PlanFeature]] = None
    is_active: Optional[bool] = None


class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    tenant_id: int
    plan_id: int
    billing_interval: BillingInterval
    starts_at: datetime
    ends_at: datetime
    auto_renew: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = None
    billing_interval: Optional[BillingInterval] = None
    auto_renew: Optional[bool] = None
    status: Optional[SubscriptionStatus] = None


class SubscriptionResponse(SubscriptionBase):
    id: int
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    canceled_at: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BillingInvoiceBase(BaseModel):
    tenant_id: int
    subscription_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    currency: str = "USD"
    description: str
    due_date: datetime
    paid_at: Optional[datetime] = None


class BillingInvoiceCreate(BillingInvoiceBase):
    pass


class BillingInvoiceUpdate(BaseModel):
    paid_at: Optional[datetime] = None
    payment_reference: Optional[str] = None


class BillingInvoiceResponse(BillingInvoiceBase):
    id: int
    status: str  # paid, unpaid, overdue
    payment_reference: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True