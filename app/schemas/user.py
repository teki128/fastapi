from app.models.user import UserBase
from typing import Union

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    hashed_password: Union[str, None] = None
    username: Union[str, None] = None