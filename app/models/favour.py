from sqlmodel import SQLModel, Field

#收藏表 增删查
class FavourBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key='user.id')
    section_id: int = Field(primary_key=True, foreign_key='section.id')

class Favour(FavourBase, table=True):
    pass

class FavourPublic(FavourBase):
    pass

class FavourCreate(FavourBase):
    pass

class FavourUpdate(FavourBase):
    pass
