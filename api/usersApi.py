import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.passwordHelpers import get_password_hash
from helpers.userHelpers import check_user, add_user_by_web, get_user_by_login, get_user_by_email, update_addressid_in_user
from helpers.addressHelpers import add_address_by_web

from database.models.UserModel import User as UserModel
from database.models.AddressModel import Address as AddressModel

from schemas.RegisterWebSchema import Register as RegisterWebSchema
from schemas.LoginSchema import Login as LoginSchema

from database.models.PostModel import Post
from database.models.WalkModel import Walk
from database.models.PinModel import Pin
from database.models.OrderModel import Order
from database.models.AnimalModel import Animal
from database.models.CommentModel import Comment
from database.models.AddressModel import Address
from database.models.FeedbackModel import Feedback
from database.models.PaymentCardModel import PaymentCard
from database.models.StatusModel import Status
from database.models.PaymentMethodModel import PaymentMethod
from database.models.PostOfficeModel import PostOffice
from database.models.OrderProductModel import OrderProduct
from database.models.ProductModel import Product
from database.models.PaymentMethodCategoryModel import PaymentMethodCategory
from database.models.PostOfficeOpenTimeModel import PostOfficeOpenTime
from database.models.SubcategoryModel import Subcategory
from database.models.BrandModel import Brand
from database.models.CategoryModel import Category

from authentication.authHandler import signJWT

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

    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=401, detail="Email already registered!")

    db_user = get_user_by_login(db=db, login=user.login)
    if db_user:
        raise HTTPException(status_code=401, detail="Login already registered!")

    user_info = add_user_by_web(db, user)
    address_info = add_address_by_web(db, user, user_info)
    update_addressid_in_user(db=db, user=user_info, address_index=address_info.id, user_index=user_info.id)

    return {"JWT Token": signJWT(user.email),
            "Address Info": address_info,   # nie wyswietla sie nwm czemu
            "User Info": user_info
            }


@router.post("/user/login/", tags=['user'], status_code=201)
async def user_login(db: Session = Depends(get_db), user: LoginSchema = Body(default=None)):
    if check_user(db, user):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail="Invalid login detail!")


@router.get("/users/", tags=['user'], status_code=201)
async def get_users():
    users = db.session.query(UserModel).all()
    return users






