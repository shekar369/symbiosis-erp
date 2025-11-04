from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel


class ConfigCategory(str, Enum):
    GENERAL = "general"
    SECURITY = "security"
    BILLING = "billing"
    EMAIL = "email"
    INTEGRATIONS = "integrations"


class ConfigValueType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    JSON = "json"


class SystemConfigBase(BaseModel):
    key: str
    value: Any
    category: ConfigCategory
    value_type: ConfigValueType
    description: str
    is_encrypted: bool = False
    is_tenant_configurable: bool = False


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    value: Any
    description: Optional[str] = None
    is_tenant_configurable: Optional[bool] = None


class SystemConfigResponse(SystemConfigBase):
    id: int

    class Config:
        from_attributes = True


class BulkConfigUpdate(BaseModel):
    configs: Dict[str, Any]