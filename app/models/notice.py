from sqlmodel import SQLModel, Field, Relationship
from typing import Union
from sqlalchemy import Column, Integer, Sequence

class NoticeBase(SQLModel):
    id: int = Field(primary_key=True, sa_column=Column(Integer, Sequence("notice_sn", start=1, increment=1), unique=True))
    title: str = Field(index=True, nullable=False)

class Notice(NoticeBase, table=True):
    content: Union[str, None] = Field(default=None)
    author_id: int = Field(foreign_key='user.id')
    # author: UserBase = Relationship(back_populates='') # TODO: 是否添加？

class NoticeCreate(Notice):
    title: str = Field(index=True, nullable=False)
    content: Union[str, None] = Field(default=None)
    author_id: int = Field(foreign_key=User.id)

