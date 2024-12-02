from typing import Annotated
from fastapi import Depends, APIRouter

from app.service.authenticate import get_current_user, get_current_admin
from app.models.notice import *
from app.models.user import UserPublic
from app.service.model_crud import notice_crud
from app.db.session import SessionDep

router = APIRouter(prefix='/api')

@router.post('/notice', response_model=NoticePublic)
async def create_notice(raw_data: NoticePreCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    data = raw_data.to_create(current_user.id)
    await notice_crud.create(data, session)
    return data

@router.delete('/notice/{notice_id}')
async def delete_notice(notice_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await notice_crud.delete(notice_id, session)

@router.get('/notice/{notice_id}', response_model=NoticePublic)
async def read_notice(notice_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await notice_crud.read(notice_id, session)

@router.get('/notice', response_model=list[NoticePublic])
async def read_all_notices(session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await notice_crud.read_all(session)

@router.patch('/notice/{notice_id}', response_model=NoticePublic)
async def update_notice(notice_id: int, data: NoticeUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await notice_crud.update(notice_id, data, session)