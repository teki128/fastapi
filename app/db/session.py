from sqlmodel import SQLModel, Session, create_engine
from app.models.user import *
from app.models.college import *
from app.models.classroom import *
from app.models.course import *
from app.models.favour import *
from app.models.notice import *
from app.models.schedule import *
from app.models.lesson import *
from app.models.section import *
from app.models.teach import *
from app.models.teacher import *
from fastapi import Depends
from typing import Annotated
from app.config.db import DBURL

engine = create_engine(DBURL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]