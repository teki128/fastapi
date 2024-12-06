from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.favour import *
from app.models.user import UserPublic
from app.db.session import SessionDep
from app.service.model_crud import favour_crud, user_crud
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.post('/favour', response_model=FavourPublic)
async def create_favour(raw_data: FavourPreCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    data = raw_data.to_create(current_user.id)
    return await favour_crud.create(data, session) # TODO: 重复添加在底层catch error，detail重复选择

@router.delete('/favour/{favour_id}')
async def delete_favour(favour_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    await favour_crud.delete(favour_id) # TODO: 鉴权机制，个人只能删除个人的favour

@router.get('/favour', response_model=Page[FavourPublic])
async def filter_favour(
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

    result = favour_crud.read_by_dict(filters, session)
    return paginate(result)