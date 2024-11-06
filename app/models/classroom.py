from sqlmodel import SQLModel, Field

class ClassroomBase(SQLModel):
    id: int = Field(primary_key=True)

class Classroom(ClassroomBase, table=True):
    building: str
    room: str

class ClassroomPublic(ClassroomBase):
    pass