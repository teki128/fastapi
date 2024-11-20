from sqlmodel import SQLModel, Field
#教室表 增删查
class ClassroomBase(SQLModel):
    building: str
    room: str

class Classroom(ClassroomBase, table=True):
    id: int = Field(primary_key=True)

class ClassroomPublic(ClassroomBase):
    pass

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(ClassroomBase):
    pass

