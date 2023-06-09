from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from app import models, schemas, oauth2
from app.database import get_db, session
from sqlalchemy import func
import json

router = APIRouter(prefix="/api/v1", tags=["posts"])


@router.get("/posts",response_model=List[schemas.PostResponse])
async def get_all_posts(
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(offset).all()
    response = [post[0].to_dict() for post in results]
    for i, vote in enumerate(results):
        response[i]["votes"] = vote[1]
    return response


@router.get("/posts/my", response_model=List[schemas.PostResponse])
async def get_my_posts(
    db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    return db.query(models.Post).filter(models.Post.user_id == current_user.id).all()


@router.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post_by_id(
    id: int,
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
async def create_post(
    payload: schemas.CreatePost,
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts("title","content","is_published") VALUES (%s,%s,%s) RETURNING *""",
    #     (payload.title, payload.content, payload.is_published),
    # )
    # post = cursor.fetchone()
    # db.commit()
    post = models.Post(user_id=current_user.id, **payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """ DELETE FROM posts WHERE id=%s RETURNING *; """,
    #     (str(id)),
    # )
    # db.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can not delete other user posts",
        )
    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int,
    payload: schemas.CreatePost,
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
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
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can not update other user posts",
        )
    update_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()
