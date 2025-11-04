from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.schemas.config import ConfigCategory, ConfigValueType


class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(JSON, nullable=False)
    category = Column(SQLAlchemyEnum(ConfigCategory), nullable=False)
    value_type = Column(SQLAlchemyEnum(ConfigValueType), nullable=False)
    description = Column(String, nullable=False)
    is_encrypted = Column(Boolean, default=False)
    is_tenant_configurable = Column(Boolean, default=False)

    def __repr__(self):
        return f"<SystemConfig(key={self.key}, category={self.category})>"


# Default system configurations
DEFAULT_CONFIGS = [
    {
        "key": "company_name",
        "value": "HR Payroll System",
        "category": ConfigCategory.GENERAL,
        "value_type": ConfigValueType.STRING,
        "description": "Company name displayed throughout the system",
        "is_encrypted": False,
        "is_tenant_configurable": False
    },
    {
        "key": "session_timeout",
        "value": 30,
        "category": ConfigCategory.SECURITY,
        "value_type": ConfigValueType.INTEGER,
        "description": "Session timeout in minutes",
        "is_encrypted": False,
        "is_tenant_configurable": False
    },
    {
        "key": "password_policy",
        "value": {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True
        },
        "category": ConfigCategory.SECURITY,
        "value_type": ConfigValueType.JSON,
        "description": "Password policy requirements",
        "is_encrypted": False,
        "is_tenant_configurable": False
    },
    {
        "key": "smtp_settings",
        "value": {
            "host": "",
            "port": 587,
            "use_tls": True,
            "username": "",
            "password": ""
        },
        "category": ConfigCategory.EMAIL,
        "value_type": ConfigValueType.JSON,
        "description": "Email server configuration",
        "is_encrypted": True,
        "is_tenant_configurable": False
    },
    {
        "key": "billing_currency",
        "value": "USD",
        "category": ConfigCategory.BILLING,
        "value_type": ConfigValueType.STRING,
        "description": "Default billing currency",
        "is_encrypted": False,
        "is_tenant_configurable": False
    },
    {
        "key": "tax_rate",
        "value": 0.0,
        "category": ConfigCategory.BILLING,
        "value_type": ConfigValueType.FLOAT,
        "description": "Default tax rate for billing",
        "is_encrypted": False,
        "is_tenant_configurable": True
    }
]