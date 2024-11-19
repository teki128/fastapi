from enum import Enum
from sqlmodel import SQLModel, Field
from app.models.section import Section
from sqlalchemy import Column, Integer, Sequence


class OddEvenEnum(str, Enum):
    NORMAL = ''
    ODD = ''
    EVEN = ''

class Weekday(int, Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 0

class ScheduleBase(SQLModel):
    id: int = Field(primary_key=True, sa_column=Column(Integer, Sequence("notice_sn", start=1, increment=1), unique=True))
    section_id: int = Field(foreign_key=Section.id)

class Schedule(ScheduleBase, table=True):
    week_start: int = Field()
    week_end: int = Field()
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field()
    period_end: int = Field()

class ScheduleCreate(Schedule):
    section_id: int = Field(foreign_key=Section.id)
    week_start: int = Field()
    week_end: int = Field()
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field()
    period_end: int = Field()

    