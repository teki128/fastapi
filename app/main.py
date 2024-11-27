from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routers import user
from app.service.router import generate_crud_routes

from app.models.lesson import Lesson, LessonCreate, LessonUpdate, LessonPublic
from app.models.college import College, CollegeCreate, CollegeUpdate, CollegePublic
from app.models.classroom import Classroom, ClassroomCreate, ClassroomUpdate, ClassroomPublic
from app.models.course import Course, CourseCreate, CourseUpdate, CoursePublic
from app.models.favour import Favour, FavourCreate, FavourUpdate, FavourPublic
from app.models.notice import Notice, NoticeCreate, NoticeUpdate, NoticePublic
from app.models.schedule import Schedule, ScheduleCreate, ScheduleUpdate, SchedulePublic
from app.models.section import Section, SectionCreate, SectionUpdate, SectionPublic
from app.models.teacher import Teacher, TeacherCreate, TeacherUpdate, TeacherPublic
from app.models.teach import Teach, TeachCreate, TeachUpdate, TeachPublic
from app.models.user import User, UserCreate, UserUpdate, UserPublic

app = FastAPI(lifespan=lifespan)

app.include_router(
    generate_crud_routes(User, UserCreate, UserUpdate, UserPublic, "user", user=True)
)

app .include_router(
    generate_crud_routes(
        Lesson, LessonCreate, LessonUpdate, LessonPublic, "lesson", read_only=False, no_update=False
    ),
)

app .include_router(
    generate_crud_routes(
        Classroom, ClassroomCreate, ClassroomUpdate, ClassroomPublic, "classroom", read_only=True
    ),
)

app .include_router(
    generate_crud_routes(
        College, CollegeCreate, CollegeUpdate, CollegePublic, "college", read_only=True
    ),
)

app.include_router(
    generate_crud_routes(
        Course, CourseCreate, CourseUpdate, CoursePublic, "course", read_only=False, no_update=True
    ),
)

app.include_router(
    generate_crud_routes(
        Favour, FavourCreate, FavourUpdate, FavourPublic, "favour", read_only=False, no_update=True
    ),
)

app.include_router(
    generate_crud_routes(
        Notice, NoticeCreate, NoticeUpdate, NoticePublic, "notice", read_only=False, no_update=False
    ),
)

app.include_router(
    generate_crud_routes(
        Schedule, ScheduleCreate, ScheduleUpdate, SchedulePublic, "schedule", read_only=False, no_update=False
    ),
)

app.include_router(
    generate_crud_routes(
        Section, SectionCreate, SectionUpdate, SectionPublic, "section", read_only=False, no_update=False
    ),
)

app.include_router(
    generate_crud_routes(
        Teach, TeachCreate, TeachUpdate, TeachPublic, "teach", read_only=False, no_update=True
    ),
)

app.include_router(
    generate_crud_routes(
        Teacher, TeacherCreate, TeacherUpdate, TeacherPublic, "teacher", read_only=True
    ),
)

app.include_router(user.router)
