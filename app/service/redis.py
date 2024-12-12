from aioredis import Redis
from app.main import app

async def set_value(key: str, value: str):
    redis: Redis = app.state.redis  # 获取 Redis 客户端
    await redis.set(key, value)
    return {"key": key, "value": value}

async def get_value(key: str):
    redis: Redis = app.state.redis  # 获取 Redis 客户端
    value = await redis.get(key, encoding='utf-8')
    return {"key": key, "value": value}