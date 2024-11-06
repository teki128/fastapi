from sqlmodel import SQLModel, Field
from typing import Union
from app.models.college import College

class UserBase(SQLModel):
    id: str = Field(primary_key=True) # TODO: id改为int，token跟随改
    username : str = Field(index=True)
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    hashed_password: str
    question: Union[str, None] = Field(default=None)
    hashed_answer: Union[str, None] = Field(default=None)
    tele: Union[int, None] = Field(default=None)
    college_id: int = Field(foreign_key=College.id)

class UserPublic(UserBase):
    pass

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    username: Union[str, None] = None
    hashed_password: Union[str, None] = None



