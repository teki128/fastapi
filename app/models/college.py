from sqlmodel import SQLModel, Field

#大学表 查
class CollegeBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

class College(CollegeBase):
    pass

class CollegePublic(CollegeBase):
    pass

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(CollegeBase):
    pass