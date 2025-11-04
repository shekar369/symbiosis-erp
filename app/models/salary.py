from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class ComponentType(str, enum.Enum):
    EARNING = "earning"
    DEDUCTION = "deduction"


class SalaryComponent(Base):
    __tablename__ = "salary_components"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    component_type = Column(Enum(ComponentType), nullable=False)
    is_fixed = Column(Integer, default=1)
    calculation_formula = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmployeeSalaryConfig(Base):
    __tablename__ = "employee_salary_configs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    salary_component_id = Column(Integer, ForeignKey("salary_components.id"), nullable=False)
    amount = Column(Float, nullable=False)
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
