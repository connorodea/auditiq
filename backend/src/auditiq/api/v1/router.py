from fastapi import APIRouter

from auditiq.api.v1.assessments import router as assessments_router
from auditiq.api.v1.auth import router as auth_router
from auditiq.api.v1.dashboard import router as dashboard_router
from auditiq.api.v1.health import router as health_router
from auditiq.api.v1.payments import router as payments_router
from auditiq.api.v1.reports import router as reports_router
from auditiq.api.v1.tenants import router as tenants_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(payments_router, prefix="/payments", tags=["payments"])
api_router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
