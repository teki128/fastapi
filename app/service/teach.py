from app.models.teach import Teach, TeachCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/teach/", response_model=Teach)
def create_teach(teach_not_safe: TeachCreate, session: SessionDep):
    db_teach = teach_not_safe.model_validate()
    session.add(db_teach)
    session.commit()
    session.refresh(db_teach)
    return db_teach

@router.get("/teach/", response_model=list[Teach])
def read_teachs(session: SessionDep):
    db_teachs = session.exec(select(Teach)).all()
    return db_teachs

@router.get("/teach/{teach_id}", response_model=Teach)
def read_teach(teach_id: int, session: SessionDep):
    db_teach = session.get(Teach, teach_id)
    if not db_teach:
        raise HTTPException(status_code=404, detail="Teach not found")
    return db_teach

@router.delete("/teach/{teach_id}", status_code=204)
def delete_teach(teach_id: int, session: SessionDep):
    db_teach = session.get(Teach, teach_id)
    if not db_teach:
        raise HTTPException(status_code=404, detail="Teach not found")
    session.delete(db_teach)
    session.commit()