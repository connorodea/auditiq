import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.engine import get_db
from auditiq.db.models.consultant import Consultant
from auditiq.services.auth import ALGORITHM

security = HTTPBearer()


async def get_current_consultant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Consultant:
    """Extract and validate JWT, return the authenticated consultant."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        consultant_id = uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    stmt = select(Consultant).where(Consultant.id == consultant_id)
    result = await db.execute(stmt)
    consultant = result.scalar_one_or_none()

    if not consultant or not consultant.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found or deactivated",
        )

    return consultant
