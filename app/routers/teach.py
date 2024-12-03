from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException

from app.models.teach import *
from app.models.user import UserPublic
from app.service.model_crud import teach_crud, teacher_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/teach/{teach_id}', response_model=TeachPublic)
async def read_teach(teach_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await teach_crud.read(teach_id, session)

@router.get('/teach', response_model=list[TeachPublic])
async def read_all_teaches(session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await teach_crud.read_all(session)

@router.get('/teach/by_teacher_name/{teacher_name}', response_model=list[TeachPublic])
async def read_teaches_by_teacher_name(teacher_name: str, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    teacher = await teacher_crud.read_by_dict({'name': teacher_name}, session)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return [teach for item in teacher for teach in item.teaches]