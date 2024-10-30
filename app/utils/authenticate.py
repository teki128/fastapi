from app.models.user import User, UserPublic
from app.schemas.token import TokenData
from data.database import fake_users_db
from typing import Union
import jwt
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.config.config import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # hashlib的上下文


def get_user(db, id: int) -> User:
    if id in db:
        user_dict = db[id]
        return User(**user_dict)

def get_user_safe(db, id: int) -> UserPublic:
    if id in db:
        user_dict = db[id]
        return UserPublic(**user_dict)
    
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

def decode_token(token):
    try:
        raw_access_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = raw_access_token.get('sub')
        if not user_id:
            return False
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        return False
    user = get_user(fake_users_db, token_data.id)
    return user

def decode_token_safe(token):
    try:
        raw_access_token = jwt.decode(token, SECRET_KEY, ALGORITHM) # decode时校验exp字段是否过期
        user_id = raw_access_token.get('sub')
        if not user_id:
            return False
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        return False
    user_safe = get_user_safe(fake_users_db, token_data.id) 
    # FIXME: schemas/token.token_data设为int报错，暂设为str
    return user_safe

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)

def authenticate_user(db, id: int, password: str):
    user = get_user(db, id)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

