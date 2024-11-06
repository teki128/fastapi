from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.lesson import Lesson
from app.models.schedule import Schedule

class CourseBase(SQLModel):
    lesson_id: int = Field(primary_key=True, foreign_key=Schedule.lesson_id)
    lesson_sn: int = Field(primary_key=True, foreign_key=Schedule.lesson_sn)

class Course(CourseBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key=User.id)