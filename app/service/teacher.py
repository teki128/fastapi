from app.models.teacher import Teacher
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.get("/teacher/", response_model=list[Teacher])
def read_teachers(session: SessionDep):
    db_teachers = session.exec(select(Teacher)).all()
    return db_teachers

@router.get("/teacher/{teacher_id}", response_model=Teacher)
def read_teacher(teacher_id: int, session: SessionDep):
    db_teacher = session.get(Teacher, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@router.delete("/teacher/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: int, session: SessionDep):
    db_teacher = session.get(Teacher, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    session.delete(db_teacher)
    session.commit()