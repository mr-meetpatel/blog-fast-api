from fastapi import FastAPI, status, HTTPException,Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,get_db,session
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    is_published: bool

@app.get("/")
async def home():
    return {"message": "Welcome..."}


@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts; """)
    posts = cursor.fetchall()
    return {"details": posts}

@app.get("/db")
def test_db_connection(db: session = Depends(get_db)):
    return {"status":"success"}

@app.get("/posts/{id}")
async def get_posts(id: int):
    cursor.execute(
        """ SELECT * FROM posts WHERE id=%s; """,
        (str(id)),
    )
    if posts := cursor.fetchone():
        return {"details": posts}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post):
    cursor.execute(
        """INSERT INTO posts("title","content","is_published") VALUES (%s,%s,%s) RETURNING *""",
        (payload.title, payload.content, payload.is_published),
    )
    post = cursor.fetchone()
    db.commit()
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(
        """ DELETE FROM posts WHERE id=%s RETURNING *; """,
        (str(id)),
    )
    db.commit()
    if post := cursor.fetchone() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )


@app.put("/posts/{id}")
async def update_post(id: int, payload: Post):
    cursor.execute(
        "UPDATE posts SET title=%s,content=%s,is_published=%s WHERE id = %s RETURNING *",
        (
            payload.title,
            payload.content,
            payload.is_published,
            str(id),
        ),
    )
    post = cursor.fetchone()
    db.commit()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    return {"details": post}
