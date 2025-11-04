from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Numeric, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.schemas.billing import BillingInterval, SubscriptionStatus


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price_monthly = Column(Numeric(10, 2), nullable=False)
    price_quarterly = Column(Numeric(10, 2), nullable=False)
    price_annual = Column(Numeric(10, 2), nullable=False)
    max_employees = Column(Integer, nullable=False)
    features = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    billing_interval = Column(SQLAlchemyEnum(BillingInterval), nullable=False)
    status = Column(SQLAlchemyEnum(SubscriptionStatus), default=SubscriptionStatus.TRIAL)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False)
    trial_end = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="subscription")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    invoices = relationship("BillingInvoice", back_populates="subscription")


class BillingInvoice(Base):
    __tablename__ = "billing_invoices"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD")
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    payment_reference = Column(String, nullable=True)
    status = Column(String, nullable=False, default="unpaid")  # paid, unpaid, overdue
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="invoices")
    subscription = relationship("Subscription", back_populates="invoices")