from sqlmodel import SQLModel, Field
from typing import Union

class UserBase(SQLModel):
    username : str = Field(index=True)

class User(UserBase, table=True):
    id: str = Field(primary_key=True)
    hashed_password: str

class UserPublic(User):
    id: str = Field(primary_key=True)


