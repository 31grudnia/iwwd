import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.breedHelpers import add_breed, get_breeds


from schemas.BreedSchema import Breed as BreedSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    BREED ENDPOINTS
"""


@router.post("/breed/add", tags=['breed'], status_code=201)
async def breed_add(breed: BreedSchema, db: Session = Depends(get_db)):
    return {"Added breed": add_breed(db=db, breed=breed)}


@router.get("/breeds", tags=['breed'], status_code=201)
async def breeds_get(db: Session = Depends(get_db)):
    return {"All breeds": get_breeds(db=db)}
