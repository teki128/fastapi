from sqlmodel import SQLModel, Field


class FavourBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key='user.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Favour(FavourBase, table=True):
    pass

class FavourCreate(FavourBase):
    user_id: int = Field(primary_key=True, foreign_key='user.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')