from typing import Annotated
from fastapi import Depends, APIRouter

from app.models.teacher import *
from app.models.user import UserPublic
from app.service.model_crud import teacher_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/teacher/{teacher_id}', response_model=TeacherPublic)
async def read_teacher(teacher_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await teacher_crud.read(teacher_id, session)

@router.get('/teacher', response_model=list[TeacherPublic])
async def read_all_teachers(session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await teacher_crud.read_all(session)