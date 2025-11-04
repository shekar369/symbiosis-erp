from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    health,
    tenants,
    employees,
    attendance,
    wage,
    leave,
    payroll,
    holidays,
    shifts,
    reports,
    admin,
    auditor,
    locations,
    templates,
    uploads,
    statutory,
    config,
    registration,
    billing,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(registration.router, prefix="/registration", tags=["registration"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(wage.router, prefix="/wages", tags=["wages"])
api_router.include_router(leave.router, prefix="/leaves", tags=["leaves"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
api_router.include_router(holidays.router, prefix="/holidays", tags=["holidays"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["shifts"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(auditor.router, prefix="/auditor", tags=["auditor"])
api_router.include_router(statutory.router, prefix="/statutory", tags=["statutory"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
