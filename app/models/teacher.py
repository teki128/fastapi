from sqlmodel import SQLModel, Field

class TeacherBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

class Teacher(TeacherBase, table=True):
    college_id: int = Field(foreign_key='college.id')