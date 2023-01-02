import fastapi
from fastapi import File, UploadFile, Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.imageHelpers import update_user_profile_image

load_dotenv(".env")
router = fastapi.APIRouter()


@router.patch("/user/profile-picture-change/{user_id}", tags=['user'], status_code=201)
async def user_update_profile_picture(user_id: int, file: UploadFile = File(), db: Session = Depends(get_db)):
    return {f"Updated user's profile picture with id {user_id}": update_user_profile_image(db=db, file=file, user_id=user_id)}






