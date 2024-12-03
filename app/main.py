from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.service.router import generate_crud_routes
from app.models.user import User, UserCreate, UserUpdate, UserPublic
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
from app.service.model_crud import user_crud, lesson_crud, college_crud, classroom_crud, course_crud, favour_crud, notice_crud, schedule_crud, section_crud, teacher_crud, teach_crud

from app.routers.user import router as user_router
from app.routers.notice import router as notice_router
from app.routers.classroom import router as classroom_router
from app.routers.college import router as college_router
from app.routers.teacher import router as teacher_router
from app.routers.teach import router as teach_router

app = FastAPI(lifespan=lifespan)

app.include_router(
    generate_crud_routes(User, UserCreate, UserUpdate, UserPublic, user_crud, "user")
)

app .include_router(
    generate_crud_routes(Lesson, LessonCreate, LessonUpdate, LessonPublic, lesson_crud, "lesson")
)

app .include_router(
    generate_crud_routes(Classroom, ClassroomCreate, ClassroomUpdate, ClassroomPublic, classroom_crud, "classroom")
)

app .include_router(
    generate_crud_routes(College, CollegeCreate, CollegeUpdate, CollegePublic, college_crud, "college")
)

app.include_router(
    generate_crud_routes(Course, CourseCreate, CourseUpdate, CoursePublic, course_crud, "course")
)

app.include_router(
    generate_crud_routes(Favour, FavourCreate, FavourUpdate, FavourPublic, favour_crud, "favour")
)

app.include_router(
    generate_crud_routes(Notice, NoticeCreate, NoticeUpdate, NoticePublic, notice_crud, "notice")
)

app.include_router(
    generate_crud_routes(Schedule, ScheduleCreate, ScheduleUpdate, SchedulePublic, schedule_crud, "schedule")
)

app.include_router(
    generate_crud_routes(Section, SectionCreate, SectionUpdate, SectionPublic, section_crud, "section")
)

app.include_router(
    generate_crud_routes(Teach, TeachCreate, TeachUpdate, TeachPublic, teach_crud, "teach")
)

app.include_router(
    generate_crud_routes(Teacher, TeacherCreate, TeacherUpdate, TeacherPublic, teacher_crud, "teacher")
)

app.include_router(user_router)
app.include_router(notice_router)
app.include_router(classroom_router)
app.include_router(college_router)
app.include_router(teacher_router)
app.include_router(teach_router)