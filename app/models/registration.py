from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.schemas.registration import RegistrationStatus


class OrganizationRegistration(Base):
    __tablename__ = "organization_registrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    business_type = Column(String, nullable=False)
    registration_number = Column(String, nullable=False, unique=True)
    tax_id = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    employee_count = Column(Integer, nullable=False)
    website = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    # Approval workflow fields
    status = Column(SQLAlchemyEnum(RegistrationStatus), default=RegistrationStatus.PENDING)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="registration")
    reviewer = relationship("User", foreign_keys=[reviewed_by])