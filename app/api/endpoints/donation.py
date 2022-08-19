from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationForUserDB
from app.services.investment import invested

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationForUserDB,
    response_model_exclude_none=True,

)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Внести пожертвования может текущий пользователь."""

    donation = await donation_crud.create(
        donation, session, user
    )
    donation_after_invested = await invested(donation, session)
    return donation_after_invested


@router.get(
    '/my',
    response_model=list[DonationForUserDB],
    response_model_exclude_none=True,

)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получает список всех пожертвований для текущего пользователя."""

    all_donations_for_user = await donation_crud.get_user_donations(
        session=session, user=user
    )
    return all_donations_for_user
