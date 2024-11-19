from sqlmodel import SQLModel, Field
from typing import Union

class SectionBase(SQLModel):
    sn: int = Field()
    lesson_id: int = Field(foreign_key='lesson.id')

class Section(SectionBase, table=True):
    id: int = Field(primary_key=True)
    capacity: int = Field()
    info: Union[str, None] = Field(default=None)
    classroom_id: int = Field(foreign_key='classroom.id')