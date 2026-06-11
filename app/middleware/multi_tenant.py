import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# Paths that do not require a resolved tenant (auth, health, docs)
_BYPASS_PATHS = {"/api/v1/auth/login", "/api/v1/auth/register", "/health", "/docs", "/redoc", "/openapi.json"}


class MultiTenantMiddleware(BaseHTTPMiddleware):
    """
    Resolves the active tenant from the X-Tenant-Slug request header and
    stores it on request.state so downstream handlers can scope DB queries.

    Tenant validation is intentionally lightweight here — the per-request
    DB session lives in the dependency layer, so we only attach the slug
    and let the CRUD layer validate it on first use.
    """

    async def dispatch(self, request: Request, call_next):
        # Skip tenant resolution for public/infrastructure paths
        if request.url.path in _BYPASS_PATHS or request.url.path.startswith("/static"):
            request.state.tenant_slug = None
            request.state.tenant_id = None
            return await call_next(request)

        tenant_slug = request.headers.get("X-Tenant-Slug")
        request.state.tenant_slug = tenant_slug
        request.state.tenant_id = None  # Resolved lazily by endpoints that need it

        if tenant_slug:
            # Lazy DB look-up: only resolve when a slug is provided.
            # We avoid a DB call on every request; endpoints that genuinely
            # require tenant isolation call _resolve_tenant() themselves.
            logger.debug("Request tenant slug: %s", tenant_slug)

        response = await call_next(request)
        return response


def get_tenant_id_from_slug(db, tenant_slug: str):
    """
    Helper used by endpoints that need the integer tenant_id from a slug.
    Returns None if the tenant does not exist or is inactive.
    """
    if not tenant_slug:
        return None
    from app.models.tenant import Tenant
    tenant = (
        db.query(Tenant)
        .filter(Tenant.slug == tenant_slug, Tenant.is_active == True)
        .first()
    )
    return tenant.id if tenant else None
