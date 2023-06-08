from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import user,post,authentication
import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        db = psycopg2.connect(
            host="172.18.0.2",
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

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)