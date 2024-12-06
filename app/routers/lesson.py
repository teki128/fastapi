from typing import Annotated, Optional
from fastapi import Depends, APIRouter, HTTPException, Query

from app.models.lesson import *
from app.models.user import UserPublic
from app.service.authenticate import get_current_user, get_current_admin
from app.service.model_crud import lesson_crud
from app.db.session import SessionDep

router = APIRouter(prefix='/api')

@router.post('/lesson', response_model=LessonPublic)
async def create_lesson(data: LessonCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await lesson_crud.create(data, session)

@router.delete('/lesson/{lesson_id}')
async def delete_lesson(lesson_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await lesson_crud.delete(lesson_id, session)

@router.get('/lesson', response_model=list[LessonPublic])
async def filter_lesson(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    name: Annotated[Optional[str], Query()] = None,
    college_id: Annotated[Optional[int], Query()] = None,
    importance: Annotated[Optional[ImportanceEnum], Query()] = None,
    exam_type: Annotated[Optional[ExamEnum], Query()] = None
):
    filters = {k: v for k, v in {
        'name': name,
        'college_id': college_id,
        'importance': importance,
        'exam_type': exam_type
    }.items() if v is not None}
    
    return await lesson_crud.read_by_dict(filters, session)

@router.patch('/lesson/{lesson_id}', response_model=LessonPublic)
async def update_lesson(lesson_id: int, data: LessonUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await lesson_crud.update(lesson_id, data, session)