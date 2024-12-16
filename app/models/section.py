from fastapi import HTTPException
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.schedule import SchedulePublic

#课序号 增删查改
class SectionBase(SQLModel):
    lesson_id: int = Field(foreign_key='lesson.id')
    capacity: int = Field(ge=0, le=200)
    info: Optional[str]
    classroom_id: int = Field(foreign_key='classroom.id')

class Section(SectionBase, table=True):
    id: int = Field(primary_key=True)
    sn: int
    lesson: 'Lesson' = Relationship(back_populates='sections')
    classroom: 'Classroom' = Relationship(back_populates='sections')
    teaches: list['Teach'] = Relationship(back_populates='sections')
    schedules: list['Schedule'] = Relationship(back_populates='section')
    courses: list['Course'] = Relationship(back_populates='section')

    def to_public(self, teacher_name, schedule, name) -> 'SectionPublic':
        return SectionPublic(
            id=self.id,
            sn=self.sn,
            lesson=self.lesson,
            capacity=self.capacity,
            info=self.info,
            classroom_id=self.classroom_id,
            lesson_id=self.lesson_id,
            teacher_names=teacher_name,
            schedule=schedule,
            name=name
        )

class SectionCreate(SectionBase):
    pass

class SectionPreCreate(SectionBase):
    teacher_id: list[int] = Field(foreign_key='teacher.id')

    async def to_create(self, sn: int) -> SectionCreate:
        return SectionCreate(
            sn=sn,
            lesson_id=self.lesson_id,
            capacity=self.capacity,
            info=self.info,
            classroom_id=self.classroom_id,
        )

class SectionPublic(SectionBase):
    id: int
    sn: int
    teacher_names: list[str]
    schedule: list[SchedulePublic] 
    name: str

class SectionUpdate(SectionBase):
    sn: Optional[int] = None
    lesson_id: int = Field(foreign_key='lesson.id', default=None)
    capacity: Optional[int] = Field(le=0, ge=200, default=None)
    info: Optional[str] = None
    classroom_id: Optional[int] = Field(foreign_key='classroom.id', default=None)

