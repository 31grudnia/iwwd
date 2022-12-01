import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv
from passlib.context import CryptContext

from database.models.UserModel import User as UserModel

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
        raise HTTPException(status_code=404, detail="Passwords dont match each other!")

    db_user = UserModel(name=user.name.title(), surname=user.surname.title(), email=user.email,
                        phone_number=user.phone_number, login=user.login, password=get_password_hash(user.password),
                        photo=None, is_admin=False, coins=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"JWT Token": signJWT(user.email),
            **user.dict()}


@router.post("/user/login/", tags=['user'], status_code=201)
async def user_login(user: LoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=404, detail="Invalid login detail!")


@router.get("/users/", tags=['user'], status_code=202)
async def get_users():
    users = db.session.query(UserModel).all()
    return users


"""
    METHODS
"""


def check_user(data: LoginSchema = Body(default=None)):
    users = db.session.query(UserModel).all()
    for user in users:
        if user.email == data.email and verify_password(data.password, user.password):
            return True
    return False


def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
