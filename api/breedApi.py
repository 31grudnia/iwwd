import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.breedHelpers import get_breeds


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    BREED ENDPOINTS
"""


@router.get("/breeds", tags=['breed'], status_code=201)
async def breeds_get(db: Session = Depends(get_db)):
    return {"All breeds": get_breeds(db=db)}
