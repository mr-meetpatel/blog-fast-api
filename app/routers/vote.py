from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from app.database import get_db, session
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["votes"])


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(
    payload: schemas.Vote,
    db: session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id==current_user.id,models.Vote.post_id==payload.post_id)
    found_vote = vote_query.first()
    if payload.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already Voted on this post")
        vote=models.Vote(post_id=payload.post_id,user_id=current_user.id)
        db.add(vote)
        message="Vote added successfully"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        message = "Vote deleted successfully"
    db.commit()
    return {"detail":message}

