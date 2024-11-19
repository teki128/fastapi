from app.models.section import Section, SectionCreate
from app.db.session import SessionDep
from fastapi import FastAPI, HTTPException
from sqlmodel import select

router = FastAPI()

@router.post("/section/", response_model=Section)
def create_section(section_not_safe: SectionCreate, session: SessionDep):
    db_section = section_not_safe.model_validate()
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section

@router.get("/section/", response_model=list[Section])
def read_sections(session: SessionDep):
    db_sections = session.exec(select(Section)).all()
    return db_sections

@router.get("/section/{section_id}", response_model=Section)
def read_section(section_id: int, session: SessionDep):
    db_section = session.get(Section, section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section

@router.delete("/section/{section_id}", status_code=204)
def delete_section(section_id: int, session: SessionDep):
    db_section = session.get(Section, section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    session.delete(db_section)
    session.commit()