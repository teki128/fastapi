from fastapi import FastAPI
from app.routers import user
from app.service import user as user_crud
from app.core.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(user_crud.router)
