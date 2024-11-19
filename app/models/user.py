from sqlmodel import SQLModel, Field
from typing import Union

class UserBase(SQLModel):
    id: int = Field(primary_key=True) # TODO: id改为int，token跟随改
    username : str = Field(index=True)
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    hashed_password: str
    question: Union[str, None] = Field(default=None)
    hashed_answer: Union[str, None] = Field(default=None)
    tele: Union[int, None] = Field(default=None)
    college_id: Union[int, None] = Field(foreign_key='college.id', default=None)

class UserPublic(UserBase):
    tele: Union[int, None] = Field(default=None)
    college_id: int = Field(foreign_key='college.id')


class UserCreate(UserBase):
    raw_password: str = Field(min_length=6)
    college_id: Union[int, None] = Field(foreign_key='college.id', default=None)

    def to_user(self, hashed_password: str) -> User:
        return User(
            id=self.id,
            username=self.username,
            is_admin=self.is_admin,
            hashed_password=hashed_password,
            question=None,
            hashed_answer=None,
            tele=None,
            college_id=self.college_id
        )


class UserUpdate(UserBase):
    raw_password: Union[str, None] = Field(min_length=6, default=None)
    question: Union[str, None] = Field(default=None)
    raw_answer: Union[str, None] = Field(default=None)
    tele: Union[int, None] = Field(default=None)
    college_id: Union[int, None] = Field(foreign_key='college.id', default=None)



