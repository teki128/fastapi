from sqlmodel import SQLModel, select
from app.db.session import SessionDep
from fastapi import HTTPException
from typing import Type, TypeVar, Generic
from app.utils.authenciate import hash_password

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
PublicSchemaType = TypeVar("PublicSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    def __init__(self, model: Type[ModelType], create_model: Type[CreateSchemaType], update_model: Type[UpdateSchemaType], public_model: Type[PublicSchemaType]):
        self.model = model
        self.create_model = create_model
        self.update_model = update_model
        self.public_model = public_model

    async def create(self, obj_in: CreateSchemaType, db: SessionDep) -> PublicSchemaType:
        validated_obj = self.create_model.model_validate(obj_in)
        db_obj = self.model(**validated_obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def read_all(self, db: SessionDep) -> list[PublicSchemaType]:
        return db.exec(select(self.model)).all()

    async def read(self, obj_id: int, db: SessionDep) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return db_obj

    async def delete(self, obj_id: int, db: SessionDep) -> None:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        db.delete(db_obj)
        db.commit()

    async def update(self, obj_id: int, obj_in: UpdateSchemaType, db: SessionDep) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDNoUpdate(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    async def update(self, obj_id: int, obj_in: UpdateSchemaType, db: SessionDep) -> PublicSchemaType:
        raise HTTPException(status_code=405, detail="Update operation is not allowed for this model")


class CRUDOnlyRead(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    async def create(self, obj_in: CreateSchemaType, db: SessionDep) -> PublicSchemaType:
        raise HTTPException(status_code=405, detail="Create operation is not allowed for this model")

    async def update(self, obj_id: int, obj_in: UpdateSchemaType, db: SessionDep) -> PublicSchemaType:
        raise HTTPException(status_code=405, detail="Update operation is not allowed for this model")

    async def delete(self, obj_id: int, db: SessionDep) -> None:
        raise HTTPException(status_code=405, detail="Delete operation is not allowed for this model")


class CRUDUser(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    async def create(self, obj_in: CreateSchemaType, db: SessionDep) -> PublicSchemaType:
        validated_obj = self.create_model.model_validate(obj_in)
        obj = validated_obj.to_user(hash_password(validated_obj.raw_password))
        db_obj = self.model(**obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(self, obj_id: int, obj_in: UpdateSchemaType, db: SessionDep) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

        update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'raw_password' and value:
                db_obj.hashed_password = hash_password(value)
            elif key == 'raw_answer' and value:
                db_obj.hashed_answer = hash_password(value)
            else:
                setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj
