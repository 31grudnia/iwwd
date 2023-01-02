import jwt
import os
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from schemas.TokenSchema import Token, TokenData
from schemas.LoginSchema import Login

from helpers.userHelpers import get_user_by_login
from helpers.passwordHelpers import get_password_hash, verify_password

load_dotenv(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET = os.environ["SECRET"]
JWT_ALGORITHM = os.environ["ALGORITHM"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#   Move to another file
def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_login(db=db, login=username)
    if not db_user:
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
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_login(db=db, login=token_data.username)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user





