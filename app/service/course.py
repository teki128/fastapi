from app.models.course import Course
from app.db.session import engine
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

app = FastAPI

@app.post("/courses/", response_model=Course)
def create_course(course: Course) -> Course:
    with Session(engine) as session:
        session.add(course)
        session.commit()
        session.refresh(course)
        return course

@app.get("/courses/", response_model=list[Course])
def read_courses():
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        return courses

@app.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int):
    with Session(engine) as session:
        course = session.get(Course, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    with Session(engine) as session:
        course = session.get(Course, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        session.delete(course)
        session.commit()
        return {"ok": True}