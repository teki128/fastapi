from app.models.notice import Notice, NoticeCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/notice/", response_model=Notice)
def create_notice(notice_not_safe: NoticeCreate, session: SessionDep):
    db_notice = notice_not_safe.model_validate()
    session.add(db_notice)
    session.commit()
    session.refresh(db_notice)
    return db_notice

@router.get("/notice/", response_model=list[Notice])
def read_notices(session: SessionDep):
    db_notices = session.exec(select(Notice)).all()
    return db_notices

@router.get("/notice/{notice_id}", response_model=Notice)
def read_notice(notice_id: int, session: SessionDep):
    db_notice = session.get(Notice, notice_id)
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return db_notice

@router.delete("/notice/{notice_id}", status_code=204)
def delete_notice(notice_id: int, session: SessionDep):
    db_notice = session.get(Notice, notice_id)
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    session.delete(db_notice)
    session.commit()