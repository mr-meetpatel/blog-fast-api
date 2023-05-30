from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from app import models, schemas, utils
from app.database import get_db, session

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/login")
def login(payload: schemas.UserLogin, db: session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(
            models.User.email == payload.email,
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not utils.pwd_context.verify(payload.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return {"message": "Login Success"}
