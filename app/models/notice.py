from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
#公告表 增删查改
class NoticeBase(SQLModel):
    title: str = Field(index=True, nullable=False)
    content: str = Field(default=None)

class Notice(NoticeBase, table=True):
    id: int = Field(primary_key=True)
    author_id: int = Field(foreign_key='user.id')

class NoticeCreate(NoticeBase):
    author_id: int = Field(foreign_key='user.id')

class NoticePreCreate(NoticeBase):
    def to_create(self, author_id: int) -> NoticeCreate:
        return NoticeCreate(
            title=self.title,
            content=self.content,
            author_id=author_id
        )

class NoticeUpdate(NoticeBase):
    title: Optional[str] = None
    content: Optional[str] = None

class NoticePublic(NoticeBase):
    id: int
    author_id: int = Field(foreign_key='user.id')

