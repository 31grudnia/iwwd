import jwt
import os
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.models.UserModel import User as UserModel
from schemas.TokenSchema import TokenData

from helpers.passwordHelpers import verify_password

load_dotenv(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET = os.environ["SECRET"]
JWT_ALGORITHM = os.environ["ALGORITHM"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


#   Move to another file
def authenticate_user(db: Session, username_email: str, password: str):
    db_user = get_user_by_email(db=db, email=username_email)
    if db_user is None:
        return False
    if not verify_password(plain_password=password, hashed_password=db_user.password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials {token}",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username_email: str = payload.get("sub")
        if username_email is None:
            raise credentials_exception
        token_data = TokenData(username_email=username_email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.username_email)
    if user is None:
        raise credentials_exception
    return user
