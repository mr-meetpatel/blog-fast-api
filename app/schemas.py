from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str


class CreatePost(Post):
    pass


class PostResponse(Post):
    id: int
    user_id: int
    is_published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str]= None
