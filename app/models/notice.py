from sqlmodel import SQLModel, Field, Relationship
from app.models.user import UserBase, User
from typing import Union

class NoticeBase(SQLModel):
    id: int = Field(primary_key=True)
    title: str = Field(index=True, nullable=False)

class Notice(NoticeBase, table=True):
    content: Union[str, None] = Field(default=None)
    author_id: int = Field(foreign_key=User.id)
    # author: UserBase = Relationship(back_populates='') # TODO: 是否添加？
