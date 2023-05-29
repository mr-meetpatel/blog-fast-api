from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db, session
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    is_published: bool


while True:
    try:
        db = psycopg2.connect(
            host="172.18.0.3",
            database="blog_db",
            user="root",
            password="root",
            cursor_factory=RealDictCursor,
        )
        cursor = db.cursor()
        print("DB Connected")
        break
    except Exception as e:
        print(f"Fail to connect DB {e}")
        time.sleep(2)


@app.get("/")
async def home():
    return {"message": "Welcome..."}


@app.get("/posts")
async def get_posts(db: session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"details": posts}


@app.get("/db")
def test_db_connection(db: session = Depends(get_db)):
    return {"status": "success"}


@app.get("/posts/{id}")
async def get_posts(id: int,db: session = Depends(get_db)):
    # cursor.execute(
    #     """ SELECT * FROM posts WHERE id=%s; """,
    #     (str(id),),
    # )
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )

    return {"details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post, db: session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts("title","content","is_published") VALUES (%s,%s,%s) RETURNING *""",
    #     (payload.title, payload.content, payload.is_published),
    # )
    # post = cursor.fetchone()
    # db.commit()
    post = models.Post(**payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: session = Depends(get_db)):
    # cursor.execute(
    #     """ DELETE FROM posts WHERE id=%s RETURNING *; """,
    #     (str(id)),
    # )
    # db.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}")
async def update_post(id: int, payload: Post,db: session = Depends(get_db)):
    # cursor.execute(
    #     "UPDATE posts SET title=%s,content=%s,is_published=%s WHERE id = %s RETURNING *",
    #     (
    #         payload.title,
    #         payload.content,
    #         payload.is_published,
    #         str(id),
    #     ),
    # )
    # post = cursor.fetchone()
    # db.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    post = update_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    update_query.update(payload.dict(),synchronize_session=False)
    db.commit()
    return {"details": update_query.first()}
