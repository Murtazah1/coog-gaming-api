'''
This is a pydantic model/schema file
made to parse inputs from the frontend
so that only the inputs I want to send are sent

'''


from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Schemas for adding and updating users


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50,
                          description="Username must be 50 characters or less")
    password: str = Field(..., max_length=100,
                          description="Password must be 100 characters or less")
    email: Optional[EmailStr] = Field(
        None,
        max_length=100,
        description="Email must be a valid email address and 100 characters or less")
    first_name: Optional[str] = Field(
        None,
        max_length=50,
        description="First name must be 50 characters or less")
    last_name: Optional[str] = Field(
        None,
        max_length=50,
        description="Last name must be 50 characters or less")
    paid_dues: Optional[bool] = Field(
        False, description="Indicates if the user has paid dues")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        max_length=50,
        description="Username must be 50 characters or less")
    password: Optional[str] = Field(
        None,
        max_length=100,
        description="Password must be 100 characters or less")
    email: Optional[EmailStr] = Field(
        None,
        max_length=100,
        description="Email must be a valid email address and 100 characters or less")
    first_name: Optional[str] = Field(
        None,
        max_length=50,
        description="First name must be 50 characters or less")
    last_name: Optional[str] = Field(
        None,
        max_length=50,
        description="Last name must be 50 characters or less")
    paid_dues: Optional[bool] = Field(
        None, description="Indicates if the user has paid dues")


# schemas for adding and updating events
