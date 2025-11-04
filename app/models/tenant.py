from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="tenant")
    employees = relationship("Employee", back_populates="tenant")
    locations = relationship("Location", back_populates="tenant")
    registration = relationship("OrganizationRegistration", back_populates="tenant", uselist=False)
    subscription = relationship("Subscription", back_populates="tenant", uselist=False)
    invoices = relationship("BillingInvoice", back_populates="tenant")
