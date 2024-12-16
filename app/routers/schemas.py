from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BaseUser(BaseModel):
    email: EmailStr

    # class Config:
    #     orm_mode = True


class CreateUser(BaseUser):
    password: str


class CreateUserResponse(BaseUser):
    datetime: datetime
    # user_exist: Optional[bool] = True


class LoginUser(BaseUser):
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class Post(BaseModel):
    title: str
    context: str
    flag: bool = None 
    ratting: Optional[int] = None
