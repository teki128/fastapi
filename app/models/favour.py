from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship

#收藏表 增删查
class FavourBase(SQLModel):
    
    section_id: int = Field(foreign_key='section.id')

class Favour(FavourBase, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    __table_args__ = (UniqueConstraint('user_id', 'section_id', name='uix_user_section_favour'),)
    section: 'Section' = Relationship(back_populates='favours')

class FavourPublic(FavourBase):
    id: int
    user_id: int = Field(foreign_key='user.id')

class FavourCreate(FavourBase):
    user_id: int = Field(foreign_key='user.id')

class FavourPreCreate(FavourBase):
    def to_create(self, user_id: int) -> FavourCreate:
        return FavourCreate(
            section_id=self.section_id,
            user_id=user_id
        )

class FavourUpdate(FavourBase):
    pass
