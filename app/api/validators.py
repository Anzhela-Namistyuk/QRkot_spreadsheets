from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
        project_id: Optional[int] = None
) -> None:
    project_id = await charity_project_crud.get_charity_project_by_name(
        project_name, session, project_id)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_invested_amount(
        project: CharityProject,
) -> None:

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'В проект были внесены средства, не подлежит удалению!'
            )
        )


def check_close_project(
        project: CharityProject
) -> None:

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'В проект были внесены средства, не подлежит удалению!'
            )
        )


def check_close_project_before_update(
        project: CharityProject
) -> None:

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Закрытый проект нельзя редактировать!'
            )
        )


def check_new_full_amount(
        project: CharityProject,
        new_obj: CharityProject,
) -> None:

    if new_obj.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                'Нельзя установить требуемую сумму меньше уже вложенной!'
            )
        )
