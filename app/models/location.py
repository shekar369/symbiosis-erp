from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class FacilityType(str, enum.Enum):
    SEZ = "SEZ"  # Special Economic Zone
    STP = "STP"  # Software Technology Park
    ASC = "ASC"  # Assessment Center
    REGULAR = "REGULAR"


class ActType(str, enum.Enum):
    CONTRACT_LABOUR = "CONTRACT_LABOUR"
    SHOPS_ESTABLISHMENT = "SHOPS_ESTABLISHMENT"
    FACTORIES = "FACTORIES"


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String(2), nullable=False, unique=True)  # AP, TG, KA, TN, MH
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    locations = relationship("Location", back_populates="state")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)  # Hyderabad, Bangalore, Pune
    city = Column(String, nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    facility_type = Column(Enum(FacilityType), default=FacilityType.REGULAR)
    act_type = Column(Enum(ActType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Address details
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String)
    postal_code = Column(String(6), nullable=False)

    # Relationships
    state = relationship("State", back_populates="locations")
    tenant = relationship("Tenant", back_populates="locations")
    employee_assignments = relationship("EmployeeLocationAssignment", back_populates="location")


class EmployeeLocationAssignment(Base):
    """Track employee location assignments over time"""
    __tablename__ = "employee_location_assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    from_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    to_date = Column(DateTime)
    is_current = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    location = relationship("Location", back_populates="employee_assignments")
