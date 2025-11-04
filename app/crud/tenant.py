from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    def get_tenant(self, db: Session, tenant_id: int) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def get_tenants(self, db: Session, skip: int = 0, limit: int = 20) -> List[Tenant]:
        return db.query(Tenant).offset(skip).limit(limit).all()

    def create_tenant(self, db: Session, tenant: TenantCreate) -> Tenant:
        return self.create(db, obj_in=tenant)

    def update_tenant(self, db: Session, tenant_id: int, tenant_update: TenantUpdate) -> Optional[Tenant]:
        db_tenant = self.get_tenant(db, tenant_id)
        if db_tenant:
            return self.update(db, db_obj=db_tenant, obj_in=tenant_update)
        return None


tenant = CRUDTenant(Tenant)
