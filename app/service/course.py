from app.models.course import Course, CourseCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/course/", response_model=Course)
def create_course(course_not_safe: CourseCreate, session: SessionDep):
    db_course = course_not_safe.model_validate();
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@router.get("/course/", response_model=list[Course])
def read_courses(session: SessionDep):
    db_courses = session.exec(select(Course)).all()
    return db_courses

@router.get("/course/{course_id}", response_model=Course)
def read_course(course_id: int, session: SessionDep):
    db_course = session.get(Course, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/course/{course_id}", status_code=204)
def delete_course(course_id: int, session: SessionDep):
    db_course = session.get(Course, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(db_course)
    session.commit()