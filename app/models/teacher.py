from sqlmodel import SQLModel, Field
from app.models.college import College

class TeacherBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

class Teacher(TeacherBase, table=True):
    college_id: int = Field(foreign_key=College.id)

class TeacherCreate(Teacher):
    pass
