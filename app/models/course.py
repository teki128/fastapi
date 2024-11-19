from sqlmodel import SQLModel, Field

#课程表
class CourseBase(SQLModel):
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Course(CourseBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key='user.id')

class CourseCreate(CourseBase):
    user_id: int = Field(primary_key=True, foreign_key='user.id')
