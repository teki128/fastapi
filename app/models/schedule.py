from enum import Enum
from sqlmodel import SQLModel, Field


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
    id: int = Field(primary_key=True)
    section_id: int = Field(foreign_key='section.id')

class Schedule(ScheduleBase, table=True):
    week_start: int = Field()
    week_end: int = Field()
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field()
    period_end: int = Field()

class ScheduleCreate(Schedule):
    section_id: int = Field(foreign_key='section.id')
    week_start: int = Field()
    week_end: int = Field()
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field()
    period_end: int = Field()

    