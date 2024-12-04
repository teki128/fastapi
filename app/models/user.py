from sqlalchemy import BigInteger
from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    id: int = Field(primary_key=True) # XXX: 尝试修改为str
    name: str
    
class UserPublic(UserBase):
    college_id: int = Field(foreign_key='college.id')
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    hashed_password: str
    question: Optional[str] = Field(default=None)
    hashed_answer: Optional[str] = Field(default=None)
    tele: Optional[int] = Field(default=None)
    college_id: Optional[int] = Field(foreign_key='college.id', default=None)
    is_admin: bool = Field(default=False)



class UserCreate(UserBase):
    raw_password: str = Field(min_length=6)
    college_id: Optional[int] = Field(foreign_key='college.id', default=None)
    is_admin: bool = Field(default=False)
    
    def to_user(self, hashed_password: str) -> User:
        return User(
            id=self.id,
            name=self.name,
            is_admin=self.is_admin,
            hashed_password=hashed_password,
            question=None,
            hashed_answer=None,
            tele=None,
            college_id=self.college_id
        )


class UserUpdate(UserBase):
    name: Optional[str] = Field(default=None)
    raw_password: Optional[str] = Field(min_length=6, default=None)
    question: Optional[str] = Field(default=None)
    raw_answer: Optional[str] = Field(default=None)
    tele: Optional[int] = Field(default=None)
    college_id: Optional[int] = Field(foreign_key='college.id', default=None)



