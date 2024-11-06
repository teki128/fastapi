from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.schedule import Schedule

class FavourBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key=User.id)
    lesson_id: int = Field(primary_key=True, foreign_key=Schedule.lesson_id)
    lesson_sn: int = Field(primary_key=True, foreign_key=Schedule.lesson_sn)

class Favour(FavourBase, table=True):
    pass