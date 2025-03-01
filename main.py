'''
This is the main code of the api
Here is where I will define all the routes

'''


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from databases import SessionLocal
from typing import Annotated


app = FastAPI()


def test_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(test_db_connection)]

# Create Read Update Delete for users

'''
@app.get("/")
def root():
    return {"hello" : "world"}
'''

# create for users


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: db_dependency):
    # small check to see if user is already made
    db_user = db.query(
        models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registerd")

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

# getting a user


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    return user

# getting multiple users


@app.get("/users/", status_code=status.HTTP_200_OK)
# skip is how many inital rows will be skipped in the query
# limit is the limit of how many rows it will return
async def get_all_users(db: db_dependency, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# updating users


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        db: db_dependency):
    db_user = db.query(
        models.User).filter(
        models.User.user_id == user_id).first()
    if db_user is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

# delete a user


@app.delete("/users/{user_id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    db.delete(user)
    db.commit()
