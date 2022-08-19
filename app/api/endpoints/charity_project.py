from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_close_project,
                                check_close_project_before_update,
                                check_invested_amount, check_name_duplicate,
                                check_new_full_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.close_update_project import close_project
from app.services.investment import invested

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session
    )
    new_project_after_invested = await invested(new_project, session)
    return new_project_after_invested


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remote_charity_projects(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    charity_projects = await check_charity_project_exists(
        project_id, session
    )

    check_close_project(charity_projects)
    check_invested_amount(charity_projects)

    charity_projects = await charity_project_crud.remove(
        charity_projects, session
    )
    return charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],

)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_close_project_before_update(charity_project)

    if obj_in.name is not None:
        await check_name_duplicate(
            obj_in.name, session, project_id
        )

    if obj_in.full_amount is not None:
        check_new_full_amount(
            charity_project, obj_in
        )

        await close_project(
            charity_project, obj_in, session
        )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    return charity_project
