from sqlmodel import SQLModel, Field
from app.models.teacher import Teacher
from app.models.schedule import Schedule

class TeachBase(SQLModel):
    teacher_id: int = Field(primary_key=True, foreign_key=Teacher.id)
    lesson_id: int = Field(primary_key=True, foreign_key=Schedule.lesson_id)
    lesson_sn: int = Field(primary_key=True, foreign_key=Schedule.lesson_sn)

class Teach(TeachBase, table=True):
    pass