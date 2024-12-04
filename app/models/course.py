from sqlmodel import SQLModel, Field, UniqueConstraint

#选课表 增删查
class CourseBase(SQLModel):
    user_id: int = Field(foreign_key='user.id')
    section_id: int = Field(foreign_key='section.id')

class Course(CourseBase, table=True):
    id: int = Field(primary_key=True)

    __table_args__ = (UniqueConstraint('user_id', 'section_id', name='uix_user_section_course'),)

class CourseCreate(CourseBase):
    pass

class CoursePublic(CourseBase):
    id: int

class CourseUpdate(CourseBase):
    pass