from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select
from app.db.session import SessionDep
from fastapi import HTTPException, status
from typing import Type, TypeVar, Generic
from app.models.teach import Teach
from app.utils.authenciate import hash_password
from app.models.schedule import Schedule, is_schedule_conflict
from app.models.section import Section
from app.models.course import Course

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
        try:
            db.commit()
            db.refresh(db_obj)
        
        except IntegrityError as e:
            db.rollback()
            if 'Duplicate entry' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Duplicate entry."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while saving the data."
                )
        return db_obj

    async def read_by_id(self, obj_id, db: SessionDep) -> ModelType:
        return db.get(self.model, obj_id)

    async def read_by_dict(self, attr: dict, db: SessionDep) -> list[ModelType]:
        query = select(self.model)
        for key, value in attr.items():
            query = query.where(getattr(self.model, key) == value)

        result = db.exec(query).all()
        # if not result:
        #     raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return result

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

class CRUDCourse(CRUDNoUpdate[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):

    async def is_course_conflict(self, db_obj: ModelType, db: SessionDep) -> bool:

        db_schedule_statement = select(Schedule).where(db_obj.section_id == Schedule.section_id)
        db_schedule_results = db.execute(db_schedule_statement)
        db_schedules = db_schedule_results.scalars().all()

        course_statement = select(self.model).where(self.model.user_id == db_obj.user_id)
        course_results = db.execute(course_statement)
        courses = course_results.scalars().all()

        section_ids = {course.section_id for course in courses}

        # 不能选同一个课程下不同课序的课
        for section_id in section_ids:
            if db.get(Section, db_obj.section_id).lesson_id == db.get(Section, section_id).lesson_id:
                return True

        schedule_statement = select(Schedule).where(Schedule.section_id.in_(section_ids))
        schedule_results = db.execute(schedule_statement)
        schedules = schedule_results.scalars().all()

        # 不能选时间表冲突的课
        for db_schedule in db_schedules:
            for schedule in schedules:
                if await is_schedule_conflict(db_schedule, schedule):
                    return True
        return False

    async def is_section_full(self, db_obj: ModelType, db: SessionDep) ->bool:
        db_section = db.get(Section, db_obj.section_id)

        if db_section == None:
            raise HTTPException(
                status_code=404,
                detail="Course not found."
            )

        db_course_statement = select(Course).where(db_obj.section_id == Course.section_id)
        db_course_results = db.execute(db_course_statement)
        db_courses = db_course_results.scalars().all()
        capacity = db_section.capacity

        num = len(db_courses)
        if num < capacity:
            return False
        else:
            return True

    async def create(self, obj_in: CreateSchemaType, db: SessionDep) -> PublicSchemaType:
        validated_obj = self.create_model.model_validate(obj_in)
        db_obj = self.model(**validated_obj.dict())

        if await self.is_section_full(db_obj, db):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Course is full."
            )

        if await self.is_course_conflict(db_obj, db):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Conflict Course."
            )
        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)

        except IntegrityError as e:
            db.rollback()
            if 'Duplicate entry' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Duplicate entry."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while saving the data."
                )

        return db_obj

class CRUDSection(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType, PublicSchemaType]):
    async def create(self, obj_in: CreateSchemaType, teacher_id: list[int], db: SessionDep) -> PublicSchemaType:
        validated_obj = self.create_model.model_validate(obj_in)
        db_obj = self.model(**validated_obj.dict())
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            for teacher in teacher_id:
                db.add(Teach(teacher_id=teacher, section_id=db_obj.id))
            db.commit()
        
        except IntegrityError as e:
            db.rollback()
            if 'Duplicate entry' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Duplicate entry."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while saving the data."
                )
        return db_obj
    
    async def read_by_dict(self, attr: dict, db: SessionDep) -> list[ModelType]:
        query = select(self.model)
        for key, value in attr.items():
            query = query.where(getattr(self.model, key) == value)

        result = db.exec(query).all()
        # if not result:
        #     raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return result
    
    async def get_next_sn(self, lesson_id: int, db: SessionDep) -> int:
        result = db.exec(select(Section).where(Section.lesson_id == lesson_id)).all()
        return len(result) + 1
    
    async def get_detail(self, raw_data: list[ModelType]) -> list[PublicSchemaType]:
        result = []
        for section in raw_data:
            teachers = [teach.teachers for teach in section.teaches]
            result.append(section.to_public(
                name=section.lesson.name, 
                teacher_name=[teacher.name for teacher in teachers], 
                schedule=section.schedules
            ))
        return result