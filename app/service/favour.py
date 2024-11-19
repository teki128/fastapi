from app.models.favour import Favour, FavourCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/favour/", response_model=Favour)
def create_favour(favour_not_safe: FavourCreate, session: SessionDep):
    db_favour = favour_not_safe.model_validate()
    session.add(db_favour)
    session.commit()
    session.refresh(db_favour)
    return db_favour

@router.get("/favour/", response_model=list[Favour])
def read_favours(session: SessionDep):
    db_favours = session.exec(select(Favour)).all()
    return db_favours

@router.get("/favour/{favour_id}", response_model=Favour)
def read_favour(favour_id: int, session: SessionDep):
    db_favour = session.get(Favour, favour_id)
    if not db_favour:
        raise HTTPException(status_code=404, detail="Favour not found")
    return db_favour

@router.delete("/favour/{favour_id}", status_code=204)
def delete_favour(favour_id: int, session: SessionDep):
    db_favour = session.get(Favour, favour_id)
    if not db_favour:
        raise HTTPException(status_code=404, detail="Favour not found")
    session.delete(db_favour)
    session.commit()