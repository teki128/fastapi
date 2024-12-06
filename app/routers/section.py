from typing import Annotated
from fastapi import Depends, Query, APIRouter
from fastapi_pagination import Page, paginate

from app.models.section import *
from app.models.user import UserPublic
from app.db.session import SessionDep
from app.service.model_crud import section_crud
from app.service.authenticate import get_current_admin, get_current_user

router = APIRouter(prefix='/api')

@router.post('/section', response_model=SectionPublic)
async def create_section(data: SectionCreate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await section_crud.create(data, session)

@router.delete('/section/{section_id}')
async def delete_section(section_id: int, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    await section_crud.delete(section_id)

@router.get('/section', response_model=Page[SectionPublic])
async def filter_section(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    id: Annotated[int, Query()] = None,
    sn: Annotated[int, Query()] = None, 
    lesson_id: Annotated[int, Query()] = None
):
    
    filters = {k: v for k, v in {
        'id': id,
        'sn': sn,
        'lesson_id': lesson_id
    }.items() if v is not None}
    result = await section_crud.read_by_dict(filters, session)    
    return paginate(result)

@router.patch('/section/{section_id}', response_model=SectionPublic)
async def update_section(section_id: int, data: SectionUpdate, session: SessionDep, current_user: Annotated[UserPublic, Depends(get_current_admin)]):
    return await section_crud.update(section_id, data, session)