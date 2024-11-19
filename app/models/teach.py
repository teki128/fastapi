from sqlmodel import SQLModel, Field

class TeachBase(SQLModel):
    teacher_id: int = Field(primary_key=True, foreign_key='teacher.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Teach(TeachBase, table=True):
    pass

class TeachCreate(Teach):
    teacher_id: int = Field(primary_key=True, foreign_key=Teacher.id)
    section_id: int = Field(primary_key=True, foreign_key=Section.id)
