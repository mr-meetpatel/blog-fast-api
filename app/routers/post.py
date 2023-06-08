from fastapi import status, HTTPException, Depends,APIRouter
from typing import List
from app import models, schemas,oauth2
from app.database import get_db, session

router = APIRouter(prefix="/api/v1",tags=["posts"])

@router.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post_by_id(id: int, db: session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
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


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(payload: schemas.CreatePost, db: session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
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


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
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


@router.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int, payload: schemas.CreatePost, db: session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)
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