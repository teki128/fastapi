from typing import Union, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError

from app.models.user import User
from app.models.token import TokenData
from app.config.config import SECRET_KEY, ALGORITHM
from app.utils.authenciate import verify_password
from app.db.session import SessionDep, Session
from app.service.user import read_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token')

async def get_user(id, session) -> User:
    user = read_user(id, session)
    return user


def create_access_token(token: dict, expire_delta: Union[timedelta, None] = None):
    raw_access_token = token.copy()
    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
    raw_access_token.update({'exp': expire_time})
    encoded_access_token = jwt.encode(raw_access_token, SECRET_KEY, ALGORITHM)
    return encoded_access_token

async def decode_token(token, session):
    try:
        raw_access_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = raw_access_token.get('sub')
        if not user_id:
            return False
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        return False
    
    user = await get_user(token_data.id, session)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep): # oauth2_scheme 提取出header里面的auth头里面的token到token参数内
    user = await decode_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def authenticate_user(id: int, password: str, session: Session):
    user = await get_user(id, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

