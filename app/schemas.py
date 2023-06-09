from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status


def is_valid_dir(value):
    if value not in [0, 1]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid value for dir.Only 0 and 1 are allow",
        )
    return value


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


class Post(BaseModel):
    title: str
    content: str


class CreatePost(Post):
    pass


class PostResponse(Post):
    id: int
    user: UserResponse
    is_published: bool = True
    created_at: datetime
    votes:int
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int
    _dir = validator("dir", allow_reuse=True)(is_valid_dir)
