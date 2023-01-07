from typing import List
from fastapi import File, UploadFile, HTTPException
from database.firebase_setup import storage
from urllib.parse import urlparse
import imghdr
import secrets

from sqlalchemy.orm import Session

from database.models.ProductImageModel import ProductImage as ProductImageModel
from database.firebase_setup import DEFAULT_USER_IMAGES

from helpers.userHelpers import get_user_by_id
from helpers.productHelpers import get_product_by_id
from authentication.authHandler import get_current_user

USER_IMAGES_FILE_PATH = "user_images/"
PRODUCT_IMAGES_FILE_PATH = "product_images/"


def find_image_by_product_id(db: Session, product_id: int):
    return db.query(ProductImageModel).filter(ProductImageModel.product_id == product_id).all()


def check_if_image(file: bytes):
    file_type = imghdr.what(None, file)
    if file_type is None:
        # The file is not an image
        raise HTTPException(status_code=412, detail="File is not image type! (imageHelpers)")
    return file_type


def delete_photo(photo_url: str):
    pass


async def update_user_profile_image(db: Session, file: File, token: str):
    user = await get_current_user(db=db, token=token)
    db_user = get_user_by_id(db=db, index=user.id)
    if db_user is None:
        raise HTTPException(status_code=412, detail="User doesnt exist! (imageHelpers)")

    if db_user.photo_url:
        parsed_url = urlparse(db_user.photo_url)
        path = parsed_url.path
        file_name = path.split("/")[-1]
        actual_file_name = file_name.split("%2F")[-1]
        if not actual_file_name in DEFAULT_USER_IMAGES:
            storage.delete(USER_IMAGES_FILE_PATH+str(actual_file_name), token=None)

    extension = check_if_image(file=file)
    token_name = secrets.token_hex(10) + "." + str(extension)
    new_file_path = USER_IMAGES_FILE_PATH + token_name
    storage.child(new_file_path).put(bytearray(file))

    image_url = storage.child(new_file_path).get_url(token=None)
    db_user.photo_url = image_url
    db.commit()
    db.refresh(db_user)

    return {"message": "Image uploaded successfully!"}


# , token: str
async def add_product_images(db: Session, files: List[File], product_id: int):
    product_check = get_product_by_id(db=db, index=product_id)
    if product_check is None:
        raise HTTPException(status_code=412, detail="Product doesnt exist! (imageHelpers)")

    old_images = find_image_by_product_id(db=db, product_id=product_id)
    for image in old_images:
        parsed_url = urlparse(image.photo_url)
        path = parsed_url.path
        file_name = path.split("/")[-1]
        actual_file_name = file_name.split("%2F")[-1]
        storage.delete(PRODUCT_IMAGES_FILE_PATH + str(actual_file_name), token=None)

    for file in files:
        extension = check_if_image(file=file)
        token_name = str(product_id) + secrets.token_hex(10) + "." + str(extension)
        new_file_path = PRODUCT_IMAGES_FILE_PATH + token_name
        storage.child(new_file_path).put(bytearray(file))
        image_url = storage.child(new_file_path).get_url(token=None)
        db_product_image = ProductImageModel(photo_url=image_url, product_id=product_id)
        db.add(db_product_image)
    db.commit()
    return {"message": "Images uploaded successfully!"}




