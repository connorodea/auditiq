from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import get_db
from auditiq.db.models.consultant import Consultant
from auditiq.db.models.tenant import Tenant
from auditiq.dependencies import get_current_consultant
from auditiq.schemas.tenant import TenantOut, TenantPublic, TenantUpdate

router = APIRouter()


@router.get("/me", response_model=TenantOut)
async def get_my_tenant(
    consultant: Consultant = Depends(get_current_consultant),
    db: AsyncSession = Depends(get_db),
) -> TenantOut:
    """Get the authenticated consultant's tenant."""
    stmt = select(Tenant).where(Tenant.id == consultant.tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return TenantOut.model_validate(tenant)


@router.patch("/me", response_model=TenantOut)
async def update_my_tenant(
    body: TenantUpdate,
    consultant: Consultant = Depends(get_current_consultant),
    db: AsyncSession = Depends(get_db),
) -> TenantOut:
    """Update the authenticated consultant's tenant branding."""
    stmt = select(Tenant).where(Tenant.id == consultant.tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tenant, field, value)

    await db.commit()
    await db.refresh(tenant)
    return TenantOut.model_validate(tenant)


@router.get("/lookup/{slug}", response_model=TenantPublic)
async def lookup_tenant(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> TenantPublic:
    """Public endpoint: look up tenant by subdomain slug.

    Used by the frontend middleware to load whitelabel config.
    """
    stmt = select(Tenant).where(Tenant.slug == slug, Tenant.is_active == True)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return TenantPublic.model_validate(tenant)
