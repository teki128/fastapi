from sqlmodel import SQLModel, Field

class CollegeBase(SQLModel):
    name: str = Field(index=True)

class College(CollegeBase, table=True):
    id: int = Field(primary_key=True)