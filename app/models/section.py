from sqlmodel import SQLModel, Field
from app.models.lesson import Lesson
from app.models.classroom import Classroom
from typing import Union
from sqlalchemy import Column, Integer, Sequence

#课序号
class SectionBase(SQLModel):
    sn: int = Field(sa_column=Column(Integer, Sequence("section_sn", start=1, increment=1), unique=True))
    lesson_id: int = Field(foreign_key=Lesson.id)

class Section(SectionBase, table=True):
    id: int = Field(primary_key=True)
    capacity: int = Field()
    info: Union[str, None] = Field(default=None)
    classroom_id: int = Field(foreign_key=Classroom.id)

class SectionCreate(Section):
    capacity: int = Field(le=0, ge=200)
    info: Union[str, None] = Field(default=None)
    classroom_id: int = Field(foreign_key=Classroom.id)
    lesson_id: int = Field(foreign_key=Lesson.id)


