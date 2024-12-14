from typing import Annotated
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.schedule import *
from app.models.user import UserPublic
from app.db.session import SessionDep
from app.service.model_crud import schedule_crud
from app.service.authenticate import get_current_admin, get_current_user

router = APIRouter(prefix='/api')

@router.post('/schedule', response_model=SchedulePublic)
async def create_schedule(data: ScheduleCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await schedule_crud.create(data, session)

@router.delete('/schedule/{schedule_id}')
async def delete_schedule(schedule_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await schedule_crud.delete(schedule_id, session)

@router.get('/schedule', response_model=Page[SchedulePublic])
async def filter_schedule(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None,
    section_id: Annotated[Optional[int], Query()] = None,
):
    
    filters = {k: v for k, v in {
        'id': id,
        'section_id': section_id
    }.items() if v is not None}

    result = await schedule_crud.read_by_dict(filters, session)    
    return paginate(result)

@router.patch('/schedule/{schedule_id}', response_model=SchedulePublic)
async def update_schedule(schedule_id: int, data: ScheduleUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await schedule_crud.update(schedule_id, data, session)