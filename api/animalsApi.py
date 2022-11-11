import fastapi
from fastapi import Depends
from fastapi_sqlalchemy import db
from dotenv import load_dotenv

from database.models.AnimalModel import Animal as AnimalModel
from schemas.AnimalSchema import Animal as AnimalSchema

from authentication.authBearer import jwtBearer

load_dotenv(".env")
router = fastapi.APIRouter()

"""
    ANIMAL ENDPOINTS
"""
@router.post("/add-animal/", dependencies=[Depends(jwtBearer())], tags=['animal'])
async def add_animal(animal: AnimalSchema):
    db_animal = AnimalModel(name=animal.name, user_id=animal.user_id)
    db.session.add(db_animal)
    db.session.commit()
    return db_animal

@router.get("/animals/")
async def get_animals():
    animals = db.session.query(AnimalModel).all()

    return animals