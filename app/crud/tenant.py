from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.utils.leave_setup import initialize_default_leave_types


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    def get_tenant(self, db: Session, tenant_id: int) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def get_tenants(self, db: Session, skip: int = 0, limit: int = 20) -> List[Tenant]:
        return db.query(Tenant).offset(skip).limit(limit).all()

    def create_tenant(self, db: Session, tenant: TenantCreate) -> Tenant:
        # Create the tenant
        new_tenant = self.create(db, obj_in=tenant)

        # Initialize default leave types for the new tenant
        initialize_default_leave_types(db, new_tenant.id)

        return new_tenant

    def update_tenant(self, db: Session, tenant_id: int, tenant_update: TenantUpdate) -> Optional[Tenant]:
        db_tenant = self.get_tenant(db, tenant_id)
        if db_tenant:
            return self.update(db, db_obj=db_tenant, obj_in=tenant_update)
        return None


tenant = CRUDTenant(Tenant)
