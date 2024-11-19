from app.models.classroom import Classroom, ClassroomCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/classroom/", response_model=Classroom)
def create_classroom(classroom_not_safe: ClassroomCreate, session: SessionDep) -> Classroom:
    db_classroom = classroom_not_safe.model_validate()
    session.add(db_classroom)
    session.commit()
    session.refresh(db_classroom)
    return db_classroom

@router.get("/classroom/", response_model=list[Classroom])
def read_classrooms(session: SessionDep):
    db_classrooms = session.exec(select(Classroom)).all()
    return db_classrooms

@router.get("/classroom/{classroom_id}", response_model=Classroom)
def read_classroom(classroom_id: int, session: SessionDep):
    db_classroom = session.get(Classroom, classroom_id)
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return db_classroom

@router.delete("/classroom/{classroom_id}", status_code=204)
def delete_classroom(classroom_id: int, session: SessionDep):
    db_classroom = session.get(Classroom, classroom_id)
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    session.delete(db_classroom)
    session.commit()