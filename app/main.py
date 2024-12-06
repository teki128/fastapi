from fastapi import FastAPI
from app.core.lifespan import lifespan

from app.routers.user import router as user_router
from app.routers.notice import router as notice_router
from app.routers.classroom import router as classroom_router
from app.routers.college import router as college_router
from app.routers.teacher import router as teacher_router
from app.routers.teach import router as teach_router
from app.routers.lesson import router as lesson_router
from app.routers.section import router as section_router

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(notice_router)
app.include_router(classroom_router)
app.include_router(college_router)
app.include_router(teacher_router)
app.include_router(teach_router)
app.include_router(lesson_router)
app.include_router(section_router)