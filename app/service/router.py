from fastapi import APIRouter
from typing import Type, TypeVar
from app.db.session import SessionDep
from sqlmodel import SQLModel
from app.service.crud import CRUDBase, CRUDOnlyRead, CRUDNoUpdate, CRUDUser

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
PublicSchemaType = TypeVar("PublicSchemaType")


def generate_crud_routes(
    model: Type[ModelType],
    create_model: Type[CreateSchemaType],
    update_model: Type[UpdateSchemaType],
    public_model: Type[PublicSchemaType],
    crud: CRUDBase,
    model_name: str,
) -> APIRouter:
    router = APIRouter()

    @router.post(f"/{model_name}/", response_model=public_model)
    async def create(
        obj_in: create_model, session: SessionDep
    ):

        return await crud.create(obj_in, session)

    @router.get(f"/{model_name}/", response_model=list[public_model])
    async def read_all(session: SessionDep):
        return await crud.read_all(session)

    @router.get(f"/{model_name}/{{obj_id}}", response_model=public_model)
    async def read(obj_id: int, session: SessionDep):
        return await crud.read(obj_id, session)

    @router.put(f"/{model_name}/{{obj_id}}", response_model=public_model)
    async def update(
        obj_id: int, obj_in: update_model, session: SessionDep
    ):
        return await crud.update(obj_id, obj_in, session)

    @router.delete(f"/{model_name}/{{obj_id}}", status_code=204)
    async def delete(obj_id: int, session: SessionDep):
        await crud.delete(obj_id, session)

    return router

# TODO: 完成上层给每个路由删除掉