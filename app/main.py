from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, authentication, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time

# Note : No need because now we are using alembic
# models.Base.metadata.create_all(bind=engine)

print(settings.ORIGINS)
app = FastAPI()

origins = settings.ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# For Reference
# while True:
#     try:
#         db = psycopg2.connect(
#             host="ip address or name",
#             database="blog_db",
#             user="user_name",
#             password="password",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = db.cursor()
#         print("DB Connected")
#         break
#     except Exception as e:
#         print(f"Fail to connect DB {e}")
#         time.sleep(2)


@app.get("/")
async def home():
    return {"message": "Welcome..."}


app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(vote.router)
