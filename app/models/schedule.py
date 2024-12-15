from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
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
    week_start: int = Field(le=18, ge=1)
    week_end: int = Field(le=18, ge=1)
    weekday: Weekday = Field()
    odd_or_even: OddEvenEnum = Field(OddEvenEnum.NORMAL)
    period_start: int = Field(le=12, ge=1)
    period_end: int = Field(le=12, ge=1)

class Schedule(ScheduleBase, table=True):
    id: int = Field(primary_key=True)

    section: 'Section' = Relationship(back_populates='schedules')

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    section_id: int = Field(foreign_key='section.id', default=None)
    week_start: Optional[int] = Field(le=1, ge=18, default=None)
    week_end: Optional[int] = Field(le=1, ge=18, default=None)
    weekday: Optional[Weekday] = None
    odd_or_even: Optional[OddEvenEnum] = None
    period_start: Optional[int] = Field(le=1, ge=12, default=None)
    period_end: Optional[int] = Field(le=1, ge=12, default=None)

class SchedulePublic(ScheduleBase):
    id: int

async def is_schedule_conflict(schedule1: Schedule, schedule2: Schedule):

    if (schedule1.week_start <= schedule2.week_end
            and schedule1.week_end >= schedule2.week_start):
        if (schedule1.odd_or_even != OddEvenEnum.NORMAL
                and schedule2.odd_or_even != OddEvenEnum.NORMAL):
            if abs(schedule1.week_start - schedule2.week_start) % 2 == 1:
                return False

        if (schedule1.weekday == schedule2.weekday
                and schedule1.period_start <= schedule1.period_end
                and schedule1.period_end >= schedule2.period_start):
            return True

    return False
