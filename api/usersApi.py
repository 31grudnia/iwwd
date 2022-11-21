import fastapi
from fastapi import Body, HTTPException
from fastapi_sqlalchemy import db
from dotenv import load_dotenv
from passlib.context import CryptContext

from database.models.UserModel import User as UserModel
from schemas.UserSchema import User as UserSchema
from schemas.RegisterWebSchema import Register as RegisterWebSchema
from schemas.LoginSchema import Login as LoginSchema

from database.models.PostModel import Post
from database.models.WalkModel import Walk
from database.models.AnimalModel import Animal
from database.models.CommentModel import Comment

from authentication.authHandler import signJWT

load_dotenv(".env")
router = fastapi.APIRouter()

"""
    USER ENDPOINTS
"""


# User Signup [ Create a new user ]
@router.post("/user/register/", tags=['user'], status_code=201)
async def user_register_web(user: RegisterWebSchema):
    if user.password != user.password_repeat:
        raise HTTPException(status_code=404, detail="Passwords dont match each other!")
    db_user = UserModel(name=user.name.title(), surname=user.surname.title(), email=user.email,
                        phone_number=user.phone_number,
                        state=user.state, city=user.city.title(), post_code=user.post_code, street=user.street.title(),
                        login=user.login, password=user.password,
                        age=18, regulations=1, sex='male', hidden_posts=0, coins=0)
    db.session.add(db_user)
    db.session.commit()
    return {"JWT Token": signJWT(user.email),
            **user.dict()}


@router.post("/user/login/", tags=['user'])
async def user_login(user: LoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=404, detail="Invalid login detail!")


@router.get("/users/", tags=['user'])
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
