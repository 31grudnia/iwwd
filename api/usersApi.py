from datetime import timedelta
import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.passwordHelpers import get_password_hash
from helpers.userHelpers import check_login_user, add_user_by_web, get_user_by_login, get_user_by_email, \
    update_addressid_in_user, get_user_by_phone_number, add_user_by_mobile
from helpers.addressHelpers import add_address_by_web
from authentication.authHandler import get_current_user, oauth2_scheme, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from database.models.UserModel import User as UserModel
from database.models.AddressModel import Address as AddressModel

from schemas.RegisterWebSchema import WebRegister as RegisterWebSchema
from schemas.RegisterMobileSchema import MobileRegister as RegisterMobileSchema
from schemas.LoginSchema import Login as LoginSchema




load_dotenv(".env")
router = fastapi.APIRouter()

"""
    USER ENDPOINTS
"""


# User Signup [ Create a new user Web ]
@router.post("/user/register/", tags=['user'], status_code=201)
async def user_register_web(user: RegisterWebSchema, db: Session = Depends(get_db)):
    if user.password != user.password_repeat:
        raise HTTPException(status_code=401, detail="Passwords dont match each other!")

    if len(user.phone_number) != 9:
        raise HTTPException(status_code=401, detail="Wrong phone number!")

    user_info = add_user_by_web(db, user)
    address_info = add_address_by_web(db, user, user_info)
    update_addressid_in_user(db=db, address_index=address_info.id, user_index=user_info.id)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"Token": access_token,
            "Address Info": address_info,   # nie wyswietla sie nwm czemu
            "User Info": user_info
            }


@router.post("/user/mobile_register", tags=['user'], status_code=201)
async def user_register_mobile(user: RegisterMobileSchema, db: Session = Depends(get_db)):
    user_info = add_user_by_mobile(db=db, user=user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"Token": access_token,
            "User Info": user_info}


# User Login [ Login as a User either to mobile app and Web ]
@router.post("/user/login/", tags=['user'], status_code=201)
async def user_login(db: Session = Depends(get_db), user: LoginSchema = Body(default=None)):
    if check_login_user(db, user):
        user_info = get_user_by_email(db=db, email=user.email)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"Tokens": access_token,
                "User Info": user_info}
    raise HTTPException(status_code=401, detail="Invalid login detail!")


# token: str = Depends(oauth2_scheme)
# Get all Users
@router.get("/users", tags=['user'], status_code=201)
async def get_users():
    users = db.session.query(UserModel).all()
    return users


@router.get("/user/me/get_id", status_code=201)
async def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = await get_current_user(db=db, token=token)
    return {"Current User's id: ": user.id}

@router.patch("/user/change_password/{recovery_token}", status_code=201)
async def change_user_password(recovery_token: str, db: Session = Depends(get_db)):
    pass






