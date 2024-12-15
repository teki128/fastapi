from typing import Annotated
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.section import *
from app.models.user import UserPublic
from app.db.session import SessionDep
from app.service.model_crud import section_crud, lesson_crud, teach_crud, schedule_crud, teacher_crud
from app.service.authenticate import get_current_admin, get_current_user

router = APIRouter(prefix='/api')

@router.post('/section', response_model=SectionPublic)
async def create_section(data: SectionPreCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await section_crud.create(data.to_create(), data.teacher_id, session)

@router.delete('/section/{section_id}')
async def delete_section(section_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await section_crud.delete(section_id, session)

@router.get('/section', response_model=Page[SectionPublic])
async def filter_section(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[int, Query()] = None,
    sn: Annotated[int, Query()] = None, 
    lesson_id: Annotated[int, Query()] = None
):
    
    filters = {k: v for k, v in {
        'id': id,
        'sn': sn,
        'lesson_id': lesson_id
    }.items() if v is not None}
    result = await section_crud.read_by_dict(filters, session)    

    for i, section in enumerate(result):
        teachers = [teach.teachers for teach in section.teaches]
        result[i] = section.to_public(
            name=section.lesson.name, 
            teacher_name=[teacher.name for teacher in teachers], 
            schedule=section.schedules
        )
    
    return paginate(result)

@router.patch('/section/{section_id}', response_model=SectionPublic)
async def update_section(section_id: int, data: SectionUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await section_crud.update(section_id, data, session)