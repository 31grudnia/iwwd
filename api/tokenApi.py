import fastapi
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv
from datetime import timedelta

from schemas.TokenSchema import Token

from authentication.authHandler import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token

load_dotenv(".env")
router = fastapi.APIRouter()


@router.post("/token", status_code=201, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username_email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
