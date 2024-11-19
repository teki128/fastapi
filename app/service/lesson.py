from app.models.lesson import Lesson, LessonCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/lesson/", response_model=Lesson)
def create_lesson(lesson_not_safe: LessonCreate, session: SessionDep):
    db_lesson = lesson_not_safe.model_validate()
    session.add(db_lesson)
    session.commit()
    session.refresh(db_lesson)
    return db_lesson

@router.get("/lesson/", response_model=list[Lesson])
def read_lessons(session: SessionDep):
    db_lessons = session.exec(select(Lesson)).all()
    return db_lessons

@router.get("/lesson/{lesson_id}", response_model=Lesson)
def read_lesson(lesson_id: int, session: SessionDep):
    db_lesson = session.get(Lesson, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

@router.delete("/lesson/{lesson_id}", status_code=204)
def delete_lesson(lesson_id: int, session: SessionDep):
    db_lesson = session.get(Lesson, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    session.delete(db_lesson)
    session.commit()