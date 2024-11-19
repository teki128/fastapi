from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.schedule import Section

#课程表
class CourseBase(SQLModel):
    section_id: int = Field(primary_key=True, foreign_key=Section.id)

class Course(CourseBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key=User.id)

class CourseCreate(Course):
    section_id: int = Field(primary_key=True, foreign_key=Section.id)
    user_id: int = Field(primary_key=True, foreign_key=User.id)