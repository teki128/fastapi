from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # hashlib的上下文

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)

def check_host_or_admin(user_id: int, current_user):
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You are not an admin or the host.")
    return current_user

def check_host_or_admin_only_admin_modify_id(data, user_id: int, current_user):
    if data.id and not current_user.is_admin: # 只有admin可以修改id
        raise HTTPException(status_code=403, detail="You are not an admin.")
    return check_host_or_admin(user_id, current_user) # 为了保持一致性，这里调用了check_host_or_admin