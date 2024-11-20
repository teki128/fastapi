from sqlmodel import SQLModel, Session, select
from fastapi import HTTPException
from typing import Type, TypeVar, Generic
from app.utils.authenciate import hash_password

# 定义泛型类型
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
PublicSchemaType = TypeVar("PublicSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: CreateSchemaType) -> PublicSchemaType:
        db_obj = obj_in.model_validate()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_all(self, db: Session) -> list[PublicSchemaType]:
        return db.exec(select(self.model)).all()

    def read(self, db: Session, obj_id: int) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return db_obj

    def delete(self, db: Session, obj_id: int) -> None:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        db.delete(db_obj)
        db.commit()

    def update(self, db: Session, obj_id: int, obj_in: UpdateSchemaType) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

        # 遍历并更新数据
        update_data = obj_in.dict(exclude_unset=True)  # 获取更新数据，排除默认值
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDUser(CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType])):
    def create(self, db: Session, obj_in: CreateSchemaType) -> PublicSchemaType:
        obj: ModelType = obj_in
        obj.hashed_password = hash_password(obj_in.hashed_password)
        db_obj = obj_in.model_validate()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, obj_id: int, obj_in: UpdateSchemaType) -> PublicSchemaType:
        db_obj = db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")

        # 遍历并更新数据
        update_data = obj_in.dict(exclude_unset=True)  # 获取更新数据，排除默认值
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
