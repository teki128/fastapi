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

class NoticePreCreate(NoticeBase):
    content: str = Field(default=None)
    
    def to_create(self, author_id: int) -> NoticeCreate:
        return NoticeCreate(
            title=self.title,
            content=self.content,
            author_id=author_id
        )

class NoticeUpdate(NoticeBase):
    title: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)

class NoticePublic(NoticeBase):
    content: str
    author_id: int = Field(foreign_key='user.id')

