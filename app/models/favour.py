from sqlmodel import SQLModel, Field, UniqueConstraint

#收藏表 增删查
class FavourBase(SQLModel):
    user_id: int = Field(foreign_key='user.id')
    section_id: int = Field(foreign_key='section.id')

class Favour(FavourBase, table=True):
    id: int = Field(primary_key=True)

    __table_args__ = (UniqueConstraint('user_id', 'section_id', name='uix_user_section'),)

class FavourPublic(FavourBase):
    pass

class FavourCreate(FavourBase):
    pass

class FavourUpdate(FavourBase):
    pass
