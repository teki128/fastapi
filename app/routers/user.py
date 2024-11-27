from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.config.config import ACCESS_TOKEN_EXPIRE_DAYS
from app.service.authenticate import authenticate_user, create_access_token
from app.service.authenticate import get_current_user
from app.models.user import UserPublic

from app.db.session import *

router = APIRouter(prefix='/api')

@router.post('/token') # 登录
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], session: SessionDep):
    user = await authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    raw_access_token = {'sub': form_data.username} 
    encoded_access_token = create_access_token(raw_access_token, timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    return {"access_token": encoded_access_token, "token_type": "bearer"} # 这里把username存入了token，json 2个字段名固定，不可更改

@router.get('/user/me', response_model=UserPublic)
async def read_users_me(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return current_user