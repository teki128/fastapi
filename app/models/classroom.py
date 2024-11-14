from sqlmodel import SQLModel, Field

class ClassroomBase(SQLModel):
    building: str
    room: str

class Classroom(ClassroomBase, table=True):
    id: int = Field(primary_key=True)

class ClassroomPublic(ClassroomBase):
    pass