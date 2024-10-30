import json

with open('app/config/db.json', 'r', encoding='utf-8') as f:
    db: dict = json.load(f)

DIALECT: str = db.get('dialect')
DRIVER: str = db.get('driver')
HOST: str = db.get('host')
PORT: int = db.get("port")
USER: str = db.get('user')
PWD: str = db.get('pwd')
DATABASE: str = db.get('database')

DBURL = f'{DIALECT}+{DRIVER}://{USER}:{PWD}@{HOST}/{DATABASE}'