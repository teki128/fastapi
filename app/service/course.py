

@app.post("/users/", response_model=User)
def create_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users/", response_model=list[User])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user: User):
    with Session(engine) as session:
        db_user = session.get(User, user.id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.name = user.name
        db_user.age = user.age
        db_user.hashed_password = user.hashed_password
        db_user.hashed_answer = user.hashed_answer
        session.commit()
        session.refresh(db_user)
        return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}