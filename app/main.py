from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

from app.core.lifespan import lifespan
from app.routers.user import router as user_router
from app.routers.notice import router as notice_router
from app.routers.classroom import router as classroom_router
from app.routers.college import router as college_router
from app.routers.teacher import router as teacher_router
from app.routers.teach import router as teach_router
from app.routers.lesson import router as lesson_router
from app.routers.section import router as section_router
from app.routers.schedule import router as schedule_router
from app.routers.course import router as course_router
from app.routers.favour import router as favour_router

app = FastAPI(lifespan=lifespan)

add_pagination(app)

origins = [
    "http://localhost:*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(notice_router)
app.include_router(classroom_router)
app.include_router(college_router)
app.include_router(teacher_router)
app.include_router(teach_router)
app.include_router(lesson_router)
app.include_router(section_router)
app.include_router(schedule_router)
app.include_router(course_router)
app.include_router(favour_router)