from pydantic import BaseModel, EmailStr
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str


class CreatePost(Post):
    pass


class PostResponse(Post):
    id: int
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
    is_active: bool =True
    created_at: datetime

    class Config:
        orm_mode = True