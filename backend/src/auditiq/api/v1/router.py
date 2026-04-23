from fastapi import APIRouter

from auditiq.api.v1.assessments import router as assessments_router
from auditiq.api.v1.health import router as health_router
from auditiq.api.v1.payments import router as payments_router
from auditiq.api.v1.reports import router as reports_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(payments_router, prefix="/payments", tags=["payments"])
