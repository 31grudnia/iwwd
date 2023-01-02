import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from api import usersApi, animalsApi, productApi, categoryApi, subcategoryApi, brandApi, breedApi, paymentMethodCategoryApi, \
    favouritesApi, imageApi, tokenApi, dbGeneratorApi

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
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],       # ['*']
                   allow_credentials=True,     # Should cookies be supported
                   allow_methods=["*"],         # POST GET etc.
                   allow_headers=["*"],
                   max_age=600)                 # Time in seconds for browsers to cache CORS responses


@app.get("/")
async def root():
    return {"message": "Hello World."}


app.include_router(usersApi.router)
app.include_router(animalsApi.router)
app.include_router(productApi.router)
app.include_router(favouritesApi.router)
app.include_router(categoryApi.router)
app.include_router(subcategoryApi.router)
app.include_router(brandApi.router)
app.include_router(breedApi.router)
app.include_router(paymentMethodCategoryApi.router)

app.include_router(tokenApi.router)
app.include_router(imageApi.router)
app.include_router(dbGeneratorApi.router)

app.mount("/static", StaticFiles(directory="static"), name="static")