from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
#公告表 增删查改
class NoticeBase(SQLModel):
    title: str = Field(index=True, nullable=False)

class Notice(NoticeBase, table=True):
    id: int = Field(primary_key=True)
    content: str
    author_id: int = Field(foreign_key='user.id')
    # author: UserBase = Relationship(back_populates='') # TODO: 是否添加？

class NoticeCreate(NoticeBase):
    content: str = Field(default=None)
    author_id: int = Field(foreign_key='user.id')

class NoticeUpdate(NoticeBase):
    title: Optional[str] = Field(index=True, nullable=False)
    content: Optional[str]

class NoticePublic(NoticeBase):
    content: str
    author_id: int = Field(foreign_key='user.id')

