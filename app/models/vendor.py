from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from datetime import datetime

from app.db.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
