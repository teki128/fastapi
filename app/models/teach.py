from sqlmodel import SQLModel, Field
from app.models.teacher import Teacher
from app.models.schedule import Section

class TeachBase(SQLModel):
    teacher_id: int = Field(primary_key=True, foreign_key=Teacher.id)
    section_id: int = Field(primary_key=True, foreign_key=Section.id)

class Teach(TeachBase, table=True):
    pass