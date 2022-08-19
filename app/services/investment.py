import datetime as dt
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

InvestedClass = Union[CharityProject, Donation]


async def invested(
        obj_model: InvestedClass,
        session: AsyncSession,

):

    if isinstance(obj_model, Donation):
        model_for_invest = CharityProject

    else:
        model_for_invest = Donation

    obj_for_invest = await session.execute(
        select(model_for_invest).where(
            model_for_invest.fully_invested.is_(False)
        ).order_by(model_for_invest.create_date)
    )

    obj_for_invest = obj_for_invest.scalars().all()
    invest_obj: InvestedClass
    now = dt.datetime.now()

    for invest_obj in obj_for_invest:
        for_invest_obj_close = (
            invest_obj.full_amount - invest_obj.invested_amount
        )
        for_obj_model_close = (
            obj_model.full_amount - obj_model.invested_amount
        )

        if for_obj_model_close >= for_invest_obj_close:
            invested_part = for_invest_obj_close
            invest_obj.fully_invested = True
            invest_obj.close_date = now
        else:
            invested_part = for_obj_model_close

        invest_obj.invested_amount += invested_part
        session.add(invest_obj)

        obj_model.invested_amount += invested_part
        if obj_model.full_amount == obj_model.invested_amount:
            obj_model.fully_invested = True
            obj_model.close_date = now
            break

    session.add(obj_model)
    await session.commit()
    await session.refresh(obj_model)
    return obj_model
