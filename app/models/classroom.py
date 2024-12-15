from sqlmodel import SQLModel, Field, Relationship
#教室表 查
class ClassroomBase(SQLModel):
    building: str
    room: str

class Classroom(ClassroomBase, table=True):
    id: int = Field(primary_key=True)
    sections: list['Section'] = Relationship(back_populates='classroom')

class ClassroomPublic(ClassroomBase):
    id: int

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(ClassroomBase):
    pass

