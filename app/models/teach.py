from sqlmodel import SQLModel, Field
#教师课程关联表 增删查
class TeachBase(SQLModel):
    teacher_id: int = Field(primary_key=True, foreign_key='teacher.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Teach(TeachBase, table=True):
    pass

class TeachCreate(TeachBase):
    pass

class TeachUpdate(TeachBase):
    pass

class TeachPublic(TeachBase):
    pass