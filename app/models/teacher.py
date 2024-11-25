from sqlmodel import SQLModel, Field
#教师表 查
class TeacherBase(SQLModel):
    name: str = Field(index=True)

class Teacher(TeacherBase, table=True):
    id: int = Field(primary_key=True)
    college_id: int = Field(foreign_key='college.id')

class TeacherCreate(TeacherBase):
   pass

class TeacherUpdate(TeacherBase):
   pass

class TeacherPublic(TeacherBase):
   college_id: int = Field(foreign_key='college.id')
