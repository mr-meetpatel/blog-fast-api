from fastapi import status, HTTPException, Depends,APIRouter
from typing import List
from app import models, schemas,utils
from app.database import get_db, session

router = APIRouter(prefix="/api/v1",tags=["users"])

@router.get("/users", response_model=List[schemas.UserResponse])
async def get_users(db: session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.post(
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

@router.get("/users/{id}", response_model=schemas.UserResponse)
async def get_user_by_id(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Result Found For Given id : {id}",
        )
    return user
