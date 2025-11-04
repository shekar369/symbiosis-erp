from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_saas_admin
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.crud.tenant import tenant as tenant_crud
from app.models.user import User

router = APIRouter()

@router.get("/dashboard")
async def tenant_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Get tenant management dashboard data"""
    total_tenants = tenant_crud.get_tenant_count(db)
    active_tenants = tenant_crud.get_tenant_count(db, is_active=True)
    pending_tenants = tenant_crud.get_tenant_count(db, is_active=False)
    
    return {
        "total_tenants": total_tenants,
        "active_tenants": active_tenants,
        "pending_tenants": pending_tenants,
        "recent_tenants": tenant_crud.get_tenants(db, limit=5)
    }

@router.post("/", response_model=TenantResponse)
async def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Create a new tenant (SaaS Admin only)"""
    existing = tenant_crud.get_tenant_by_name(db, name=tenant.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Tenant with this name already exists"
        )
    return tenant_crud.create_tenant(db=db, tenant=tenant)

@router.get("/", response_model=List[TenantResponse])
async def list_tenants(
    skip: int = 0,
    limit: int = 20,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """List all tenants with optional status filter"""
    if status:
        is_active = status.lower() == "active"
        return tenant_crud.get_tenants_by_status(db, is_active=is_active, skip=skip, limit=limit)
    return tenant_crud.get_tenants(db=db, skip=skip, limit=limit)

@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    """Get a specific tenant by ID"""
    tenant = tenant_crud.get_tenant(db=db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    tenant_update: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_saas_admin)
):
    tenant = tenant_crud.update_tenant(db=db, tenant_id=tenant_id, tenant_update=tenant_update)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
