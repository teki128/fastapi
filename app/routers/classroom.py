from typing import Annotated
from fastapi import Depends, APIRouter

from app.models.classroom import *
from app.models.user import UserPublic
from app.service.model_crud import classroom_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/classroom/{classroom_id}', response_model=ClassroomPublic)
async def read_classroom(classroom_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await classroom_crud.read(classroom_id, session)

@router.get('/classroom', response_model=list[ClassroomPublic])
async def read_all_classrooms(session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await classroom_crud.read_all(session)