from sqlmodel import SQLModel, Field

class TeacherBase(SQLModel):
    name: str = Field(index=True)

class Teacher(TeacherBase, table=True):
    id: int = Field(primary_key=True)
    college_id: int = Field(foreign_key='college.id')
