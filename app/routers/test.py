from typing import Annotated, Union
from fastapi import APIRouter, Query, Cookie
from app.schemas.test import Test

router = APIRouter()

@router.get('/class/test')
def test(name: Annotated[str, Query(max_length=20)], 
        user_id: Annotated[Union[str, None], Cookie()] = None,
        test: Annotated[Union[str, None], Query(max_length=20)] = None,
    ):
    return {'name': name, 'user_id': user_id, 'test': test}

@router.put('/class/update/{id}')
def update(data: Test):
    return {'data': data}