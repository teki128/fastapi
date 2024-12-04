from typing import Annotated, Optional
from fastapi import Depends, APIRouter, Query

from app.models.classroom import *
from app.models.user import UserPublic
from app.service.model_crud import classroom_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')

@router.get('/classroom', response_model=list[ClassroomPublic])
async def filter_classroom(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None
):
    filters = {k: v for k, v in {
        'id': id,
    }.items() if v is not None}

    return await classroom_crud.read_by_dict(filters, session)