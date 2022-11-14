import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from api import usersApi, animalsApi
load_dotenv(".env")

app = FastAPI(
    title="iWalkWithDog",
    description="Application to help getting with home animals.",
    version="0.0.1",
    contact={
        "name": "Mikolaj",
        "email": "mikolaj.starczewski@pollub.edu.pl",
    },
      license_info={
        "name": "GRYMAS",
    }
)

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def root():
    return {"message": "Hello World."}

app.include_router(usersApi.router)
app.include_router(animalsApi.router)


