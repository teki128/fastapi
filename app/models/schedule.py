from enum import Enum
from sqlmodel import SQLModel, Field
from app.models.lesson import Lesson
from app.models.classroom import Classroom
from typing import Union

class OddEvenEnum(str, Enum):
    NORMAL = ''
    ODD = ''
    EVEN = ''

class ScheduleBase(SQLModel):
    lesson_id: int = Field(primary_key=True, foreign_key=Lesson.id)
    lesson_sn: int = Field(primary_key=True)

class Schedule(ScheduleBase, table=True):
    week_start: int = Field()
    week_end: int = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    section_start: int = Field()
    section_end: int = Field()
    info: Union[str, None] = Field(default=None)
    building: str = Field(foreign_key=Classroom.building)
    room: str = Field(foreign_key=Classroom.room)