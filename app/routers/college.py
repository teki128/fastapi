from typing import Annotated
from fastapi import Depends, APIRouter

from app.models.college import *
from app.models.user import UserPublic
from app.service.model_crud import college_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/college/{college_id}', response_model=CollegePublic)
async def read_college(college_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await college_crud.read(college_id, session)

@router.get('/college', response_model=list[CollegePublic])
async def read_all_colleges(session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await college_crud.read_all(session)