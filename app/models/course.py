from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.schedule import Section

#课程表  增删查
class CourseBase(SQLModel):
    section_id: int = Field(primary_key=True, foreign_key=Section.id)

class Course(CourseBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key=User.id)

class Course_Public(CourseBase):
    user_id: int = Field(primary_key=True, foreign_key=User.id)

class CourseCreate(CourseBase):
    user_id: int = Field(primary_key=True, foreign_key=User.id)

class CourseUpdate(CourseBase):
    pass