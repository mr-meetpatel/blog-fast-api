from fastapi import FastAPI, status, HTTPException, Depends
from passlib.context import CryptContext
from typing import List
from psycopg2.extras import RealDictCursor
from . import models, schemas,utils
from .database import engine, get_db, session
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        db = psycopg2.connect(
            host="172.20.0.2",
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


@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post_by_id(id: int, db: session = Depends(get_db)):
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

    return post


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(payload: schemas.CreatePost, db: session = Depends(get_db)):
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
async def delete_post(id: int, db: session = Depends(get_db)):
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


@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int, payload: schemas.CreatePost, db: session = Depends(get_db)
):
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
    update_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()

@app.get("/users", response_model=List[schemas.UserResponse])
async def get_users(db: session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(payload: schemas.User, db: session = Depends(get_db)):
    password = utils.pwd_context.hash(payload.password)
    payload.password = password
    user = models.User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{id}", response_model=schemas.UserResponse)
async def get_user_by_id(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    return user
