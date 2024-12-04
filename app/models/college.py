from sqlmodel import SQLModel, Field

#系表 查
class CollegeBase(SQLModel):
    name: str = Field(index=True)

class College(CollegeBase, table=True):
    id: int = Field(primary_key=True)

class CollegePublic(CollegeBase):
    id: int

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(CollegeBase):
    pass