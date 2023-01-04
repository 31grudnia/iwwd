from typing import List
import fastapi
from fastapi import File, UploadFile, Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.imageHelpers import update_user_profile_image, add_product_images
from authentication.authHandler import oauth2_scheme

load_dotenv(".env")
router = fastapi.APIRouter()


@router.patch("/user/profile-picture-change", tags=['user'], status_code=201)
async def user_update_profile_picture(file: bytes = File(...), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    image_response = await update_user_profile_image(db=db, file=file, token=token)
    return {f"Updated user's profile picture.": image_response}


@router.post("/user/{prodyct_id}/product-image-add", tags=['product'], status_code=201)
async def product_add_pictures(product_id: int, file: List[bytes] = File(...), db: Session = Depends(get_db)):
    image_response = await add_product_images(db=db, files=file, product_id=product_id)
    return {f"Updated product pics with id {product_id}.": image_response}





