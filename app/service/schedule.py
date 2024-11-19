from app.models.schedule import Schedule, ScheduleCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/schedule/", response_model=Schedule)
def create_schedule(schedule_not_safe: ScheduleCreate, session: SessionDep):
    db_schedule = schedule_not_safe.model_validate()
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule

@router.get("/schedule/", response_model=list[Schedule])
def read_schedules(session: SessionDep):
    db_schedules = session.exec(select(Schedule)).all()
    return db_schedules

@router.get("/schedule/{schedule_id}", response_model=Schedule)
def read_schedule(schedule_id: int, session: SessionDep):
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@router.delete("/schedule/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: int, session: SessionDep):
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    session.delete(db_schedule)
    session.commit()