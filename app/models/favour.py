from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.lesson import Lesson

class FavourBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key=User.id)
    lesson_id: int = Field(primary_key=True, foreign_key=Lesson.id)

class Favour(FavourBase, table=True):
    pass