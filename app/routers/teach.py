from typing import Annotated, Optional
from fastapi import Depends, Query, APIRouter, HTTPException

from app.models.teach import *
from app.models.user import UserPublic
from app.service.model_crud import teach_crud, teacher_crud
from app.db.session import SessionDep
from app.service.authenticate import get_current_user

router = APIRouter(prefix='/api')
@router.get('/teach', response_model=list[TeachPublic])
async def filter_teach(
    session: SessionDep, 
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[Optional[int], Query()] = None,
    teacher_id: Annotated[Optional[int], Query()] = None,
    section_id: Annotated[Optional[int], Query()] = None,
):
    filters = {k: v for k, v in {
        'id': id,
        'teacher_id': teacher_id,
        'section_id': section_id
    }.items() if v is not None}

    teach = await teach_crud.read_by_dict(filters, session)
    return teach