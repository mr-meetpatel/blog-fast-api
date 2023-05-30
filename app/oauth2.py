from jose import JWTError,jwt
from datetime import datetime,timedelta

SECRET_KEY = "9e90aca1f7ea37cb2b7f1a78a7e9ac6b1f616e8f2361fdbb828c7c412b7b33c3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire_time
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
