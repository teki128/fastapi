from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.course import *
from app.models.user import UserPublic
from app.service.model_crud import section_crud
from app.db.session import SessionDep
from app.service.model_crud import course_crud, user_crud
from app.service.authenticate import get_current_admin, get_current_user
from app.utils.authenciate import check_host_or_admin

router = APIRouter(prefix='/api')

@router.post('/course', response_model=list[CoursePublic])
async def create_course_for_myself(raw_data: list[CoursePreCreate], session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    result = []
    for each_raw_data in raw_data:
        each_data = each_raw_data.to_create(current_user.id)
        course = await course_crud.create(each_data, session)

        user = await user_crud.read_by_id(each_data.user_id, session)
        section = await section_crud.read_by_id(each_data.section_id, session)
        teachers = [teach.teachers for teach in section.teaches]
        section_public = section.to_public(
            name=section.lesson.name,
            teacher_name=[teacher.name for teacher in teachers],
            schedule=section.schedules
        )
        course_public = course.to_public(user, section_public)
        result.append(course_public)
    return result

@router.post('/course/admin', response_model=CoursePublic)
async def create_course_for_user(
    data: list[CourseCreate],
    session: SessionDep,
    current_admin: Annotated[UserPublic, Depends(get_current_admin)]
):
    for each_data in data:
        course = await course_crud.create(each_data, session)

        user = await user_crud.read_by_id(each_data.user_id, session)
        section = await section_crud.read_by_id(each_data.section_id, session)
        teachers = [teach.teachers for teach in section.teaches]
        section_public = section.to_public(
            name=section.lesson.name,
            teacher_name=[teacher.name for teacher in teachers],
            schedule=section.schedules
        )
        course_public = course.to_public(user, section_public)

    return course_public

@router.delete('/course/')
async def delete_course(course_id: list[int], session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    for each_course_id in course_id:
        course = await course_crud.read_by_id(each_course_id, session)
        if check_host_or_admin(course.user_id, current_user):
            await course_crud.delete(course_id, session) 

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

    sections = [course.section for course in result]
    users = [course.user for course in result]
    
    for i, course in enumerate(result):
        result[i] = course.to_public(users[i], (await section_crud.get_detail([sections[i]]))[0])

    return paginate(result) 
