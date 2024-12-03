from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship


#教师课程关联表 增删查
class TeachBase(SQLModel):
    teacher_id: int = Field(foreign_key='teacher.id')
    section_id: int = Field(foreign_key='section.id')

class Teach(TeachBase, table=True):
    id: int = Field(primary_key=True)
    teacher: list['Teacher'] = Relationship(back_populates="teaches")

    __table_args__ = (UniqueConstraint('teacher_id', 'section_id', name='uix_teacher_section'),)

class TeachCreate(TeachBase):
    pass

class TeachUpdate(TeachBase):
    pass

class TeachPublic(TeachBase):
    pass