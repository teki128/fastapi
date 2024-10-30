import json

with open('app/config/crypt.json', 'r', encoding='utf-8') as f:
    crypt: dict = json.load(f)

SECRET_KEY: str = crypt.get('secret_key')
ALGORITHM: str = crypt.get('algorithm')
ACCESS_TOKEN_EXPIRE_DAYS: int = crypt.get('access_token_expire_days')

