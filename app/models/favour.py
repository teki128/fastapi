from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.schedule import Section

class FavourBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key=User.id)
    section_id: int = Field(primary_key=True, foreign_key=Section.id)

class Favour(FavourBase, table=True):
    pass

class FavourPublic(FavourBase):
   pass

class FavourCreate(FavourBase):
    pass

class FavourUpdate(FavourBase):
    pass
