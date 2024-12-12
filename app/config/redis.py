import json

with open('app/config/redis.json', 'r', encoding='utf-8') as f:
    redis: dict = json.load(f)

DRIVER: str = redis.get('driver')
HOST: str = redis.get('host')
PWD: str = redis.get('pwd')
PORT: int = redis.get("port")
DB: str = redis.get('db')

REDISURL = f'{DRIVER}://{HOST}'