from sqlmodel import SQLModel, Field, Relationship
from typing import Union

class NoticeBase(SQLModel):
    title: str = Field(index=True, nullable=False)

class Notice(NoticeBase, table=True):
    id: int = Field(primary_key=True)
    content: Union[str, None] = Field(default=None)
    author_id: int = Field(foreign_key='user.id')
    # author: UserBase = Relationship(back_populates='') # TODO: 是否添加？

class NoticeCreate(NoticeBase):
    title: str = Field(index=True, nullable=False)
    content: Union[str, None] = Field(default=None)
    author_id: int = Field(foreign_key='user.id')

