import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.config import settings
from auditiq.db.models.consultant import Consultant
from auditiq.db.models.tenant import Tenant

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(consultant_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(consultant_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])


def _generate_slug(company_name: str) -> str:
    """Generate a URL-safe slug from company name."""
    import re
    slug = company_name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:63]


async def register_consultant(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str,
    company_name: str,
) -> tuple[Consultant, str]:
    """Register a new consultant with their own tenant.

    Returns (consultant, access_token).
    """
    # Check email not taken
    stmt = select(Consultant).where(Consultant.email == email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    # Create tenant for this consultant
    slug = _generate_slug(company_name)

    # Ensure slug is unique
    base_slug = slug
    counter = 1
    while True:
        stmt = select(Tenant).where(Tenant.slug == slug)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    tenant = Tenant(
        slug=slug,
        name=company_name,
        cta_text=f"Powered by {company_name}",
    )
    db.add(tenant)
    await db.flush()

    # Create consultant
    consultant = Consultant(
        tenant_id=tenant.id,
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        company_name=company_name,
    )
    db.add(consultant)
    await db.commit()
    await db.refresh(consultant)

    token = create_access_token(consultant.id)
    return consultant, token


async def login_consultant(
    db: AsyncSession,
    email: str,
    password: str,
) -> tuple[Consultant, str]:
    """Authenticate consultant. Returns (consultant, access_token)."""
    stmt = select(Consultant).where(Consultant.email == email)
    result = await db.execute(stmt)
    consultant = result.scalar_one_or_none()

    if not consultant or not verify_password(password, consultant.password_hash):
        raise ValueError("Invalid email or password")

    if not consultant.is_active:
        raise ValueError("Account is deactivated")

    token = create_access_token(consultant.id)
    return consultant, token
