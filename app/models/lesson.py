from sqlmodel import SQLModel, Field
from enum import Enum

class ImportanceEnum(str, Enum):
    HIGH = ''
    MEDIUM = ''
    LOW = '' # TODO:记得改备注

class ExamEnum(str, Enum):
    EXAM = ''
    TEST = ''

class LessonBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)


class Lesson(LessonBase, table=True):
    college_id: int = Field(foreign_key='college.id')
    credit: int
    study_time: int
    importance: ImportanceEnum = Field(default=ImportanceEnum.HIGH) 
    exam_type: ExamEnum = Field(default=ExamEnum.EXAM)
