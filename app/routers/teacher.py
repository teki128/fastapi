from typing import Annotated, Optional
from fastapi import Depends, APIRouter, Query

from app.models.teacher import *
from app.models.user import UserPublic
from app.service.model_crud import teacher_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/teacher', response_model=list[TeacherPublic]) # TODO: 重构所有的get型api路径，切换为Query型api
async def filter_teacher(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)], 
    id: Annotated[Optional[int], Query()] = None,
    name: Annotated[Optional[str], Query()] = None,
    college_id: Annotated[Optional[int], Query()] = None
):
    filters = {k: v for k, v in {
        'id': id,
        'name': name,
        'college_id': college_id
    }.items() if v is not None}

    return await teacher_crud.read_by_dict(filters, session)
