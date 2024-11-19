from app.models.college import College
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.get("/college/", response_model=list[College])
def read_colleges(session: SessionDep):
    db_colleges = session.exec(select(College)).all()
    return db_colleges

@router.get("/college/{college_id}", response_model=College)
def read_college(college_id: int, session: SessionDep):
    db_college = session.get(College, college_id)
    if not db_college:
        raise HTTPException(status_code=404, detail="College not found")
    return db_college

@router.delete("/college/{college_id}", status_code=204)
def delete_college(college_id: int, session: SessionDep):
    db_college = session.get(College, college_id)
    if not db_college:
        raise HTTPException(status_code=404, detail="College not found")
    session.delete(db_college)
    session.commit()