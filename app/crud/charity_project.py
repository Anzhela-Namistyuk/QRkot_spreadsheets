from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
            project_id: Optional[int] = None
    ) -> Optional[int]:
        select_project_id = select(CharityProject.id).where(
            CharityProject.name == project_name
        )
        if project_id is not None:
            select_project_id = select_project_id.where(
                CharityProject.id != project_id
            )
        db_charity_project_id = await session.execute(select_project_id)
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        charity_projects = await session.execute(
            select([CharityProject.name,
                    CharityProject.description,
                    CharityProject.create_date,
                    CharityProject.close_date]).where(
                CharityProject.fully_invested == True
            ).order_by(
                extract('year', CharityProject.close_date) -
                extract('year', CharityProject.create_date),
                extract('month', CharityProject.close_date) -
                extract('month', CharityProject.create_date),
                extract('day', CharityProject.close_date) -
                extract('day', CharityProject.create_date),
                extract('hour', CharityProject.close_date) -
                extract('hour', CharityProject.create_date),
                extract('minute', CharityProject.close_date) -
                extract('minute', CharityProject.create_date),
                extract('second', CharityProject.close_date) -
                extract('second', CharityProject.create_date),
            )
        )

        charity_projects = charity_projects.all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
