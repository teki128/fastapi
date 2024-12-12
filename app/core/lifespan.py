from app.db.session import create_db_and_tables
from fastapi import FastAPI
from aioredis import Redis
from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.config.redis import REDISURL


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    
    app.state.redis = await Redis.from_url(REDISURL, encoding='utf-8', decode_responses=True)
    yield

    await app.state.redis.close()