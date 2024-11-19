from sqlmodel import SQLModel, Field

class CollegeBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

class College(CollegeBase, table=True):
    pass