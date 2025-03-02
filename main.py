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

# logger imports
from logger import logger
from middleware import log_req
from exceptions import exception_handler

app = FastAPI()

# adding middleware and the exception handler
app.middleware("http")(log_req)
app.add_exception_handler(HTTPException, exception_handler)


def test_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(test_db_connection)]


# root endpoint
@app.get("/")
def root():
    logger.info("root endpoint accessed")
    return {"hello": "world"}


# Create Read Update Delete for users


# create for users


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: db_dependency):
    # small check to see if user is already made
    logger.info(f"Attempting to create user with email: {user.email}")

    db_user = db.query(
        models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        logger.warning(f"User with email {user.email} already exists")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registerd")

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

    # sending a log and json of the newly created user
    db.refresh(db_user)
    logger.info(f"User created successfully with ID: {db_user.user_id}")
    return db_user

# getting a user


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    logger.info(f"Fetching user with ID: {user_id}")
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")

    logger.info(f"User with ID {user_id} fetched successfully")
    return user

# getting multiple users


@app.get("/users/", status_code=status.HTTP_200_OK)
# skip is how many inital rows will be skipped in the query
# limit is the limit of how many rows it will return
async def get_all_users(db: db_dependency, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching all users with skip={skip} and limit={limit}")
    users = db.query(models.User).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(users)} users successfully")
    return users

# updating users


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        db: db_dependency):
    logger.info(f"Attempting to update user with ID: {user_id}")
    db_user = db.query(
        models.User).filter(
        models.User.user_id == user_id).first()
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")

    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    logger.info(f"User with ID {user_id} updated successfully")
    return db_user

# delete a user


@app.delete("/users/{user_id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_user(user_id: int, db: db_dependency):
    logger.info(f"Attempting to delete user with ID: {user_id}")
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        logger.warning(f"User with ID {user_id} not found")
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    db.delete(user)
    db.commit()
    logger.info(f"User with ID {user_id} deleted successfully")
    return {"message": "User deleted successfully"}
