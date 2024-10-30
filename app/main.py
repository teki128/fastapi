from fastapi import FastAPI
from app.routers import test, user
from app.core.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(test.router)
app.include_router(user.router)
