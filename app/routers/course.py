from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.course import *
from app.models.user import UserPublic
from app.db.session import SessionDep
from app.service.model_crud import course_crud, user_crud
from app.service.authenticate import get_current_admin, get_current_user

router = APIRouter(prefix='/api')

@router.post('/course', response_model=CoursePublic)
async def create_course_for_myself(raw_data: CoursePreCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    data = raw_data.to_create(current_user.id)
    return await course_crud.create(data, session) # TODO: 选课注意时间冲突

@router.post('/course/admin', response_model=CoursePublic)
async def create_course_for_user(
    data: CourseCreate,
    session: SessionDep,
    current_admin: Annotated[UserPublic, Depends(get_current_admin)]
):
    return await course_crud.create(data, session)

@router.delete('/course/{course_id}')
async def delete_course(course_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    await course_crud.delete(course_id) # TODO: 鉴权机制，个人只能删除个人的course

@router.get('/course', response_model=Page[CoursePublic])
async def filter_course(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None,
    user_id: Annotated[Optional[int], Query()] = None,
    section_id: Annotated[Optional[int], Query()] = None,
):
    
    filters = {k: v for k, v in {
        'id': id,
        'user_id': user_id,
        'section_id': section_id,
        
    }.items() if v is not None}

    result = await course_crud.read_by_dict(filters, session)
    return paginate(result)