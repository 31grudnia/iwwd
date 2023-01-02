from fastapi import File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image
import secrets

from sqlalchemy.orm import Session

from database.models.UserModel import User as UserModel

from helpers.userHelpers import get_user_by_id

FILE_PATH = "./static/images/"


def get_user_image_by_id(db: Session, index: int):
    return db.query(UserModel).filter(UserModel.id == index).first()


def check_if_image(extension: str):
    if extension not in ["png", "jpg"]:
        raise HTTPException(status_code=412, detail="Wrong file format! (imageHelpers)")


def update_user_profile_image(db: Session, file: File, user_id: int):
    db_user = get_user_by_id(db=db, index=user_id)
    if db_user is None:
        raise HTTPException(status_code=412, detail="User doesnt exist! (imageHelpers)")
    filename = file.filename
    extension = filename.split(".")[1]
    check_if_image(extension=extension)

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILE_PATH + "user/" + token_name
    file_content = file.file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)
    img.close()

    db_user.photo = file_content
    db.commit()
    db.refresh(db_user)

    file_url = "localhost:8000" + generated_name[1:]
    return FileResponse(file_url)



