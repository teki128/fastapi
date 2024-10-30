from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends
from typing import Annotated
from app.config.db import DBURL

engine = create_engine(DBURL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]