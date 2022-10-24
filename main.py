import os
import uvicorn
from fastapi import FastAPI, Body, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from models import User
from schema import User as SchemaUser
from schema import Login as SchemaLogin
from models import Animal
from schema import Animal as SchemaAnimal

from authentication.authHandler import signJWT
from authentication.authBearer import jwtBearer

load_dotenv(".env")

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def root():
    return {"message": "Hello World."}

"""
    USER ENDPOINTS
"""

# User Signup [ Create a new user ]
@app.post("/user/signup/", tags=['user'])
async def user_signup(user: SchemaUser = Body(default=None)):
    db_user = User(name=user.name, surname=user.surname, city=user.city, email=user.email, age=user.age, phone_number=user.phone_number, login=user.login, password=user.password, photo=user.photo, regulations=user.regulations, sex=user.sex, hidden_posts=user.hidden_posts, friends=user.friends)
    db.session.add(db_user)     # TD; password to hash
    db.session.commit()
    return signJWT(user.email)

@app.post("/user/login/", tags=['user'])
async def user_login(user: SchemaLogin = Body(default=None)):
    if checkUser(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }

def checkUser(data: SchemaUser = Body(default=None)):
    users = db.session.query(User).all()
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.get("/users/")
async def get_users():
    users = db.session.query(User).all()
    return users

"""
    ANIMAL ENDPOINTS
"""
@app.post("/add-animal/", dependencies=[Depends(jwtBearer())], tags=['animal'])
async def add_animal(animal: SchemaAnimal):
    db_animal = Animal(name=animal.name, user_id=animal.user_id)
    db.session.add(db_animal)
    db.session.commit()
    return db_animal

@app.get("/animals/")
async def get_animals():
    animals = db.session.query(Animal).all()

    return animals