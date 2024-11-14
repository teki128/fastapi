from app.models.classroom import Classroom
from app.db.session import engine
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

app = FastAPI()

@app.post("/classrooms/", response_model=Classroom)
def create_classroom(classroom: Classroom) -> Classroom:
    with Session(engine) as session:
        session.add(classroom)
        session.commit()
        session.refresh(classroom)
        return classroom

@app.get("/classrooms/", response_model=list[Classroom])
def read_classrooms():
    with Session(engine) as session:
        classrooms = session.exec(select(Classroom)).all()
        return classrooms

@app.get("/classrooms/{classroom_id}", response_model=Classroom)
def read_classroom(classroom_id: int):
    with Session(engine) as session:
        classroom = session.get(Classroom, classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")
        return classroom

@app.delete("/classrooms/{classroom_id}")
def delete_classroom(classroom_id: int):
    with Session(engine) as session:
        classroom = session.get(Classroom, classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")
        session.delete(classroom)
        session.commit()
        return {"ok": True}