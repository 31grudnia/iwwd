import fastapi
from fastapi import File, UploadFile, Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.imageHelpers import update_user_profile_image
from authentication.authHandler import oauth2_scheme

load_dotenv(".env")
router = fastapi.APIRouter()

# TD get current user, delete img not used

@router.patch("/user/profile-picture-change", tags=['user'], status_code=201)
async def user_update_profile_picture(file: bytes = File(...), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    image_response = await update_user_profile_image(db=db, file=file, token=token)
    return {f"Updated user's profile picture.": image_response}






