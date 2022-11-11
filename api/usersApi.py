import fastapi
from fastapi import Body
from fastapi_sqlalchemy import db
from dotenv import load_dotenv
from passlib.context import CryptContext

from database.models.UserModel import User as UserModel
from schemas.UserSchema import User as UserSchema
from schemas.LoginSchema import Login as LoginSchema

from authentication.authHandler import signJWT

load_dotenv(".env")
router = fastapi.APIRouter()


"""
    USER ENDPOINTS
"""

# User Signup [ Create a new user ]
@router.post("/user/signup/", tags=['user'])
async def user_signup(user: UserSchema = Body(default=None)):
    user.password = get_password_hash(user.password)
    db_user = UserModel(name=user.name, surname=user.surname, city=user.city, email=user.email, age=user.age, phone_number=user.phone_number, login=user.login, password=user.password, photo=user.photo, regulations=user.regulations, sex=user.sex, hidden_posts=user.hidden_posts, friends=user.friends)
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