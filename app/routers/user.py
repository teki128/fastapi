from typing import Annotated
from fastapi import Depends, Query, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, paginate
from datetime import timedelta
from app.utils.authenciate import verify_password

from app.config.config import ACCESS_TOKEN_EXPIRE_DAYS
from app.service.authenticate import authenticate_user, create_access_token
from app.service.authenticate import get_current_user, get_current_admin
from app.service.model_crud import user_crud
from app.db.session import *

router = APIRouter(prefix='/api')

@router.post('/user', response_model=UserPublic)
async def create_user(data: UserCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await user_crud.create(data, session)

@router.delete('/user/{user_id}')
async def delete_user(user_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await user_crud.delete(user_id, session)

@router.get('/user', response_model=Page[UserPublic])
async def filter_user(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_admin)],
    id: Annotated[Optional[int], Query()] = None,
    name: Annotated[Optional[str], Query()] = None,
    college_id: Annotated[Optional[int], Query()] = None
):

    filters = {k: v for k, v in {
        'id': id,
        'name': name,
        'college_id': college_id
    }.items() if v is not None}

    result = await user_crud.read_by_dict(filters, session)
    return paginate(result) # TODO: 需添加一个读取主键返回xxpublic对象的api端点

@router.get('/user/me', response_model=UserPublic)
async def read_myself(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return current_user

@router.post('/user/forgot-password')
async def check_answer(user_id: int, answer: str, data: UserUpdate, session: SessionDep):
    db_user = await user_crud.read_by_id(user_id, session)
    if not db_user:
        HTTPException(status_code=401, detail="Incorrect username")

    if verify_password(answer, db_user.hashed_answer):
        await reset_password(user_id, data, session)
    else:
        raise HTTPException(status_code=500, detail="Answer is fail")

# 传输数据的时候只要传递raw_password属性即可
@router.patch('/user/reset-password', response_model=UserPublic)
async def reset_password(data: UserUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return await user_crud.update_password(current_user.id, data, session)

@router.patch('/user/{user_id}', response_model=UserPublic)
async def update_user(data: UserUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_user)]):
    data.id = current_user.id
    return await user_crud.update(current_user.id, data, session)

@router.post('/token') # 登录
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], session: SessionDep):
    user = await authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    raw_access_token = {'sub': form_data.username} 
    encoded_access_token = create_access_token(raw_access_token, timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    return {"access_token": encoded_access_token, "token_type": "bearer"} # 这里把username存入了token，json 2个字段名固定，不可更改

