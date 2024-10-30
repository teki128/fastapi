from app.db.session import create_db_and_tables
from fastapi import FastAPI


def start_up():
    create_db_and_tables()

async def lifespan(app: FastAPI):
    start_up()
    yield