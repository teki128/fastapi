from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
#课程表 增删查改
class ImportanceEnum(str, Enum):
    HIGH = '必修'
    MEDIUM = '选修'
    LOW = '其它'

class ExamEnum(str, Enum):
    EXAM = '考试'
    TEST = '考查'

class LessonBase(SQLModel):
    name: str = Field(index=True)
    college_id: int = Field(foreign_key='college.id')
    credit: int
    study_time: int
    importance: ImportanceEnum = Field(default=ImportanceEnum.HIGH) 
    exam_type: ExamEnum = Field(default=ExamEnum.EXAM)

class Lesson(LessonBase, table=True):
    id: int = Field(primary_key=True)
    sections: list['Section']  = Relationship(back_populates='lesson')

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    name: Optional[str] = None
    college_id: Optional[int] = Field(foreign_key='college.id', default=None)
    credit: Optional[int] = None
    study_time: Optional[int] = None
    importance: Optional[ImportanceEnum] = None
    exam_type: Optional[ExamEnum] = None

class LessonPublic(LessonBase):
    id: int
    sections: list['Section']  = Relationship(back_populates='lesson')