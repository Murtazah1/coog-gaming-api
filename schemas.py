'''
This is a pydantic model/schema file made to parse inputs from the frontend so that only the inputs I want to send are sent

'''



from pydantic import BaseModel
from typing import Optional


# schemas for adding and updating users

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    paid_dues: Optional[bool] = False

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    paid_dues: Optional[bool] = False


# schemas for adding and updating events