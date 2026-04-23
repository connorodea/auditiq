from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import get_db
from auditiq.dependencies import get_current_consultant
from auditiq.db.models.consultant import Consultant
from auditiq.schemas.consultant import (
    AuthResponse,
    ConsultantLogin,
    ConsultantOut,
    ConsultantRegister,
    ConsultantUpdate,
)
from auditiq.services.auth import login_consultant, register_consultant

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(
    body: ConsultantRegister,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    try:
        consultant, token = await register_consultant(
            db=db,
            email=body.email,
            password=body.password,
            full_name=body.full_name,
            company_name=body.company_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return AuthResponse(
        access_token=token,
        consultant=ConsultantOut.model_validate(consultant),
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    body: ConsultantLogin,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    try:
        consultant, token = await login_consultant(
            db=db,
            email=body.email,
            password=body.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return AuthResponse(
        access_token=token,
        consultant=ConsultantOut.model_validate(consultant),
    )


@router.get("/me", response_model=ConsultantOut)
async def get_me(
    consultant: Consultant = Depends(get_current_consultant),
) -> ConsultantOut:
    return ConsultantOut.model_validate(consultant)


@router.patch("/me", response_model=ConsultantOut)
async def update_me(
    body: ConsultantUpdate,
    consultant: Consultant = Depends(get_current_consultant),
    db: AsyncSession = Depends(get_db),
) -> ConsultantOut:
    if body.full_name is not None:
        consultant.full_name = body.full_name
    if body.company_name is not None:
        consultant.company_name = body.company_name
    await db.commit()
    await db.refresh(consultant)
    return ConsultantOut.model_validate(consultant)
