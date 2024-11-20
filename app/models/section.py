from sqlmodel import SQLModel, Field
from typing import Union
from sqlalchemy import Column, Integer, Sequence

#课序号
class SectionBase(SQLModel):
    sn: int = Field()
    lesson_id: int = Field(foreign_key='lesson.id')

class Section(SectionBase, table=True):
    id: int = Field(primary_key=True)
    capacity: int = Field()
    info: Union[str, None] = Field(default=None)
    classroom_id: int = Field(foreign_key='classroom.id')

class SectionCreate(SectionBase):
    capacity: int = Field(le=0, ge=200)
    info: Union[str, None] = Field(default=None)
    classroom_id: int = Field(foreign_key='classroom.id')
    lesson_id: int = Field(foreign_key='lesson.id')


