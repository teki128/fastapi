from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional

#课程时间表 增删查改
class OddEvenEnum(str, Enum):
    NORMAL = '正常'
    ODD = '单周'
    EVEN = '双周'

class Weekday(int, Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 0

class ScheduleBase(SQLModel):
    section_id: int = Field(foreign_key='section.id')
    week_start: int = Field(le=1, ge=18)
    week_end: int = Field(le=1, ge=18)
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field(le=1, ge=12)
    period_end: int = Field(le=1, ge=12)

class Schedule(ScheduleBase, table=True):
    id: int = Field(primary_key=True)


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(ScheduleBase):
    week_start: Optional[int] = Field(le=1, ge=18)
    week_end: Optional[int] = Field(le=1, ge=18)
    weekday: Optional[Weekday] = Field()
    odd_or_even: Optional[OddEvenEnum] = Field(OddEvenEnum.NORMAL)
    period_start: Optional[int] = Field(le=1, ge=12)
    period_end: Optional[int] = Field(le=1, ge=12)

class SchedulePublic(ScheduleBase):
    pass
    