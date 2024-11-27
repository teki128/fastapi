from fastapi import APIRouter, HTTPException
from app.models.user import *
from app.utils.authenciate import hash_password
from app.db.session import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post('/user/', response_model=UserPublic)
def create_user(user_not_safe: UserCreate, session: SessionDep) -> UserPublic:
    user = user_not_safe.to_user(hash_password(user_not_safe.raw_password))
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete('/user/{user_id}', status_code=204)
def delete_user(user_id: int, session: SessionDep): 
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(db_user)
    session.commit()


@router.get('/user/', response_model=list[UserPublic])
def read_users(session: SessionDep):
    db_users = session.exec(select(User)).all()
    return db_users


@router.get('/user/{user_id}', response_model=UserPublic)
def read_user_safe(user_id: int, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user: 
        raise HTTPException(status_code=404, detail='User not found')
    
    return db_user

@router.get('/user/unsafe/{user_id}', response_model=User)
def read_user(user_id: int, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user: 
        raise HTTPException(status_code=404, detail='User not found')
    
    return db_user

@router.patch('/user/{user_id}', response_model=UserPublic)
def update_user(user_id: int, new_user_not_safe: UserUpdate, session: SessionDep) -> UserPublic:
    db_user = session.get(User, user_id)
    if not db_user: 
        raise HTTPException(status_code=404, detail='User not found')
    
    new_user_not_safe_data: dict = new_user_not_safe.model_dump(exclude_unset=True)
    for key, value in new_user_not_safe_data.items():
        if key == 'raw_password' and value:
            db_user.hashed_password = hash_password(value)
        elif key == 'raw_answer' and value:
            db_user.hashed_answer = hash_password(value)
        else:
            setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user