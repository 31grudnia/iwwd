import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.paymentMethodHelpers import get_payment_methods


load_dotenv(".env")
router = fastapi.APIRouter()


"""
    PAYMENT METHOD ENDPOINTS
"""


@router.get("/payment_methods", tags=['payment_method'], status_code=201)
async def payment_methods_get(db: Session = Depends(get_db)):
    return {"Payment Methods": get_payment_methods(db=db)}