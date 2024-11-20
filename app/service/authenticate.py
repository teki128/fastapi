import httpx
from app.models.user import User, UserPublic
from app.models.token import TokenData
from typing import Union, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
from app.config.config import SECRET_KEY, ALGORITHM
from app.utils.authenciate import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token')

async def get_user(id) -> User:
    client = httpx.AsyncClient()
    response = await client.get(f"http://localhost:8000/user/unsafe/{id}")
    if response.status_code == 200:
        user_data = response.json()
    else:
        return False
    user = User(**user_data)
    return user

async def get_user_safe(id) -> UserPublic:
    client = httpx.AsyncClient()
    response = await client.get(f"http://localhost:8000/user/{id}")
    if response.status_code == 200:
        user_data = response.json()
    else:
        return False
    user_safe = UserPublic(**user_data)
    return user_safe
# 获取user

def create_access_token(token: dict, expire_delta: Union[timedelta, None] = None):
    raw_access_token = token.copy()
    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
    raw_access_token.update({'exp': expire_time})
    encoded_access_token = jwt.encode(raw_access_token, SECRET_KEY, ALGORITHM)
    return encoded_access_token

async def decode_token(token):
    try:
        raw_access_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = raw_access_token.get('sub')
        if not user_id:
            return False
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        return False
    
    user = await get_user(token_data.id)
    return user

async def decode_token_safe(token):
    try:
        raw_access_token = jwt.decode(token, SECRET_KEY, ALGORITHM) # decode时校验exp字段是否过期
        user_id = raw_access_token.get('sub')
        if not user_id:
            return False
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        return False
    
    user_safe = await get_user_safe(token_data.id)
    return user_safe


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): # oauth2_scheme 提取出header里面的auth头里面的token到token参数内
    user = await decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_user_safe(token: Annotated[str, Depends(oauth2_scheme)]):
    user_safe = await decode_token_safe(token)
    if not user_safe:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_safe


async def authenticate_user(id: int, password: str):
    user = await get_user(id)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

