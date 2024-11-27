from fastapi import HTTPException
from sqlmodel import select

from app.models.user import *
from app.utils.authenciate import hash_password
from app.db.session import Session


def create_user(user_not_safe: UserCreate, session: Session) -> UserPublic:
    user = user_not_safe.to_user(hash_password(user_not_safe.raw_password))
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(user_id: int, session: Session): 
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(db_user)
    session.commit()


def read_users(session: Session):
    db_users = session.exec(select(User)).all()
    return db_users

def read_user(user_id: int, session: Session):
    db_user = session.get(User, user_id)
    if not db_user: 
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

def update_user(user_id: int, new_user_not_safe: UserUpdate, session: Session) -> UserPublic:
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