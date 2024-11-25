from fastapi import APIRouter
from typing import Type, TypeVar
from app.db.session import SessionDep
from sqlmodel import SQLModel
from app.service.crud import CRUDBase, CRUDOnlyRead, CRUDNoUpdate

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
PublicSchemaType = TypeVar("PublicSchemaType")


def generate_crud_routes(
    model: Type[ModelType],
    create_model: Type[CreateSchemaType],
    update_model: Type[UpdateSchemaType],
    public_model: Type[PublicSchemaType],
    model_name: str,
    read_only: bool = False,
    no_update: bool = False
) -> APIRouter:
    router = APIRouter()

    if read_only:
        crud = CRUDOnlyRead(model, create_model, update_model, public_model)
    elif no_update:
        crud = CRUDNoUpdate(model, create_model, update_model, public_model)
    else:
        crud = CRUDBase(model, create_model, update_model, public_model)

    if not read_only:
        @router.post(f"/{model_name}/", response_model=public_model)
        def create(
            obj_in: create_model, session: SessionDep
        ):
            return crud.create(session, obj_in)

    @router.get(f"/{model_name}/", response_model=list[public_model])
    def read_all(session: SessionDep):
        return crud.read_all(session)

    @router.get(f"/{model_name}/{{obj_id}}", response_model=public_model)
    def read(obj_id: int, session: SessionDep):
        print('test')
        print(obj_id)
        return crud.read(session, obj_id)

    if not read_only and not no_update:
        @router.put(f"/{model_name}/{{obj_id}}", response_model=public_model)
        def update(
            obj_id: int, obj_in: update_model, session: SessionDep
        ):
            return crud.update(session, obj_id, obj_in)

    if not read_only:
        @router.delete(f"/{model_name}/{{obj_id}}", status_code=204)
        def delete(obj_id: int, session: SessionDep):
            crud.delete(session, obj_id)

    return router
