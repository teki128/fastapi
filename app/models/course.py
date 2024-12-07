from sqlmodel import SQLModel, Field, UniqueConstraint, select

#选课表 增删查
class CourseBase(SQLModel):
    section_id: int = Field(foreign_key='section.id')

class Course(CourseBase, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    __table_args__ = (UniqueConstraint('user_id', 'section_id', name='uix_user_section_course'),)

class CourseCreate(CourseBase):
    user_id: int = Field(foreign_key='user.id')

class CoursePreCreate(CourseBase):
    def to_create(self, user_id: int) -> CourseCreate:
        return CourseCreate(
            section_id=self.section_id,
            user_id=user_id
        )


class CoursePublic(CourseBase):
    id: int
    user_id: int = Field(foreign_key='user.id')

class CourseUpdate(CourseBase):
    pass