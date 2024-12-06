from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.college import *
from app.models.user import UserPublic
from app.service.model_crud import college_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/college', response_model=Page[CollegePublic])
async def filter_college(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None,
    name: Annotated[Optional[str], Query()] = None
):
    filters = {k: v for k, v in {
        'id': id,
        'name': name
    }.items() if v is not None}

    result = await college_crud.read_by_dict(filters, session)
    return paginate(result)
