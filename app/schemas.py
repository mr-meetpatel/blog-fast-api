from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


class CreatePost(Post):
    pass


class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
