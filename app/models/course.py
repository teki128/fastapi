from sqlmodel import SQLModel, Field

class CourseBase(SQLModel):
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Course(CourseBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key='user.id')