from sqlalchemy.orm import Session
from fastapi import Body, HTTPException

from authentication.authHandler import get_current_user
from helpers.addressHelpers import get_address_by_id
from helpers.passwordHelpers import get_password_hash, verify_password

from database.models.UserModel import User as UserModel
from database.models.AddressModel import Address as AddressModel

from schemas.RegisterMobileSchema import MobileRegister as RegisterMobileSchema
from schemas.LoginSchema import Login as LoginSchema
from schemas.RegisterWebSchema import WebRegister as RegisterWebSchema
from schemas.UserUpadteSchema import UserUpdate as UserUpadteSchema
from schemas.UserUpdatePasswordSchema import UserUpdatePassword as UserUpdatePasswordSchema


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


async def update_user(db: Session, userSchema: UserUpadteSchema, token: str):
    if len(userSchema.phone_number) != 9:
        raise HTTPException(status_code=402, detail="Wrong phone number given! (userHelpers file)")

    user = await get_current_user(db=db, token=token)
    db_user = get_user_by_id(db=db, index=user.id)
    
    db_user.name = userSchema.name.title()
    db_user.surname = userSchema.surname.title()
    db_user.phone_number = userSchema.phone_number

    db_address = get_address_by_id(db=db, index=db_user.address_id)
    if db_address is None:
        db_address = AddressModel(city=userSchema.city, street=userSchema.street, state=userSchema.state, home_number=
                                  userSchema.home_number, post_code=userSchema.post_code, user_id=user.id)
        db.add(db_address)
        db.commit()
        db_user.address_id = db_address.id
    else:
        db_address.city = userSchema.city
        db_address.street = userSchema.street
        db_address.state = userSchema.state
        db_address.home_number = userSchema.home_number
        db_address.post_code = userSchema.post_code
    db.commit()
    db.refresh(db_user)
    db.refresh(db_address)
    return {"User": db_user,
            "Address": db_address}


async def update_user_password_by_web(db: Session, userSchema: UserUpdatePasswordSchema, token: str):
    user = await get_current_user(db=db, token=token)

    if verify_password(plain_password=userSchema.old_password, hashed_password=user.password):
        db_user = get_user_by_id(db=db, index=user.id)
        db_user.password = get_password_hash(userSchema.new_password)
        db.commit()
        db.refresh(db_user)
    else:
        raise HTTPException(status_code=402, detail="Old password doesnt match! (userHelpers file)")


def check_login_user(db: Session, data: LoginSchema = Body(default=None)):
    db_user = get_user_by_email(db=db, email=data.email)
    if db_user is None:
        raise HTTPException(status_code=402, detail="User not found in database! (userHelpers file)")
    if not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=402, detail="Wrong password! (userHelpers file)")
    return True
