from typing import Annotated
from app.config.config import ACCESS_TOKEN_EXPIRE_DAYS
from app.service.authenticate import authenticate_user, create_access_token
from app.service.authenticate import get_current_user_safe
from app.models.user import User
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from data.database import fake_users_db
from datetime import timedelta

router = APIRouter(prefix='/api')

@router.post('/token') # 登录
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    raw_access_token = {'sub': form_data.username} 
    encoded_access_token = create_access_token(raw_access_token, timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    return {"access_token": encoded_access_token, "token_type": "bearer"} # 这里把username存入了token，json 2个字段名固定，不可更改

@router.get('/user/me', response_model=User)
def read_users_me(current_user: Annotated[User, Depends(get_current_user_safe)]):
    return current_user