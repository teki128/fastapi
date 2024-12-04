from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter

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

@router.get('/notice', response_model=list[NoticePublic])
async def filter_notice(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None, 
    title: Annotated[Optional[int], Query()] = None
):
    filters = {k: v for k, v in {
        'id': id,
        'title': title
    }.items() if v is not None}

    return await notice_crud.read_by_dict(filters, session)

@router.patch('/notice/{notice_id}', response_model=NoticePublic)
async def update_notice(notice_id: int, data: NoticeUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await notice_crud.update(notice_id, data, session)