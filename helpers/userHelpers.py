from sqlalchemy.orm import Session
from fastapi import Body, HTTPException

from helpers.passwordHelpers import get_password_hash, verify_password

from database.models.UserModel import User as UserModel

from schemas import RegisterWebSchema, RegisterMobileSchema, LoginSchema


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_id(db: Session, index: int):
    return db.query(UserModel).filter(UserModel.id == index).first()


def get_user_by_login(db: Session, login: str):
    return db.query(UserModel).filter(UserModel.login == login).first()


def get_user_by_recovery_token(db: Session, token: str):
    return db.query(UserModel).filter(UserModel.recovery_token == token).first()


def get_user_by_phone_number(db: Session, phone_num: str):
    if len(phone_num) == 9:
        return db.query(UserModel).filter(UserModel.phone_number == phone_num).first()
    raise HTTPException(status_code=402, detail="Wrong phone number given! (userHelpers file)")


def add_user_by_web(db: Session, user: RegisterWebSchema):
    db_user = get_user_by_phone_number(db=db, phone_num=user.phone_number)
    if db_user:
        raise HTTPException(status_code=401, detail="Phone number exists!")

    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=401, detail="Email already registered!")

    db_user = get_user_by_login(db=db, login=user.login)
    if db_user:
        raise HTTPException(status_code=401, detail="Login already registered!")

    db_user = UserModel(name=user.name.title(), surname=user.surname.title(), email=user.email,
                        phone_number=user.phone_number, login=user.login, password=get_password_hash(user.password),
                        photo_url="https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/user_images%2Fprofile_picture_man.png?alt=media&token=03c86f39-2a32-4892-8e39-16a79c8cf45e",
                        coins=0, favourites=[])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_user_by_mobile(db: Session, user: RegisterMobileSchema):
    check_login = get_user_by_login(db=db, login=user.login)
    if check_login:
        raise HTTPException(status_code=401, detail="Login already registered! (userHelpers file)")

    check_email = get_user_by_email(db=db, email=user.email)
    if check_email:
        raise HTTPException(status_code=401, detail="Email already registered! (userHelpers file)")

    db_user = UserModel(email=user.email, login=user.login, password=get_password_hash(user.password),
                        photo_url="https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/user_images%2Fprofile_picture_man.png?alt=media&token=03c86f39-2a32-4892-8e39-16a79c8cf45e",
                        coins=0, favourites=[])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_addressid_in_user(db: Session, address_index: int, user_index: int):
    user_to_update = get_user_by_id(db=db, index=user_index)
    if not user_to_update:
        HTTPException(status_code=402, detail="User NOT found in database! (userHelpers file)")
    setattr(user_to_update, 'address_id', address_index)
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update


def delete_user_by_id(db: Session, user_id: int):
    check_user = get_user_by_id(db=db, index=user_id)
    if check_user is None:
        raise HTTPException(status_code=402, detail="User doesnt exist! (userHelpers file)")
    db.delete(check_user)
    db.commit()
    return {"message": "Record successfully deleted"}


def check_login_user(db: Session, data: LoginSchema = Body(default=None)):
    db_user = get_user_by_email(db=db, email=data.email)
    if db_user is None:
        raise HTTPException(status_code=402, detail="User not found in database! (userHelpers file)")
    if not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=402, detail="Wrong password! (userHelpers file)")
    return True
