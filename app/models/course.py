from sqlmodel import SQLModel, Field

#选课表 增删查
class CourseBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key='user.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Course(CourseBase, table=True):
    pass

class CourseCreate(CourseBase):
    pass

class CoursePublic(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass