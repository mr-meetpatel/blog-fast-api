from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models, schemas, utils,oauth2
from app.database import get_db, session

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(
            models.User.email == payload.username,
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
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token": access_token,"token_type":"Bearer"}
