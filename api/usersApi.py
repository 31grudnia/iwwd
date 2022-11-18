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
    db_user = UserModel(name=user.name, surname=user.surname, email=user.email, phone_number=user.phone_number,
                        state=user.state, city=user.city, post_code=user.post_code, street=user.street,
                        login=user.login, password=user.password,
                        age=18, regulations=1, sex='male', hidden_posts=0, coins=0)
    db.session.add(db_user)
    db.session.commit()
    return db_user, signJWT(user.email)

@router.post("/user/add/", tags=['user'])
async def user_add(user: UserSchema = Body(default=None)):
    user.password = get_password_hash(user.password)
    db_user = UserModel(name=user.name, surname=user.surname, city=user.city, email=user.email, age=user.age, phone_number=user.phone_number, login=user.login, password=user.password, photo=user.photo, regulations=user.regulations, sex=user.sex, hidden_posts=user.hidden_posts, friends=user.friends, coins=user.coins)
    db.session.add(db_user)
    db.session.commit()
    return signJWT(user.email)

@router.post("/user/login/", tags=['user'])
async def user_login(user: LoginSchema = Body(default=None)):
    if checkUser(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }


@router.get("/users/")
async def get_users():
    users = db.session.query(UserModel).all()
    return users

"""
    HELP METHODS
"""
def checkUser(data: UserSchema = Body(default=None)):
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