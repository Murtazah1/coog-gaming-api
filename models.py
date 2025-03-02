'''
This is a sqlalchemy file
used to make the models that correspond to tables in the database

'''


from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from databases import Base


# model for users
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    email = Column(String(255), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    signup_date = Column(TIMESTAMP, default=func.now())
    paid_dues = Column(Boolean, default=False)


# model for events
