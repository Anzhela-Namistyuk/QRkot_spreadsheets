import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject


async def close_project(
        obj_model: CharityProject,
        obj_in: CharityProject,
        session: AsyncSession,
):
    now = dt.datetime.now()

    if obj_model.invested_amount == obj_in.full_amount:
        obj_model.fully_invested = True
        obj_model.close_date = now
        session.add(obj_model)
        await session.commit()
        await session.refresh(obj_model)
