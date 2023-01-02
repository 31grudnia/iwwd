import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.paymentMethodHelpers import add_payment_method, get_payment_methods

from schemas.PaymentMethodSchema import PaymentMethod as PaymentMethodSchema


load_dotenv(".env")
router = fastapi.APIRouter()


"""
    PAYMENT METHOD ENDPOINTS
"""


@router.post("/payment_method/add", tags=['payment_method'], status_code=201)
async def payment_method_add(payment_method: PaymentMethodSchema, db: Session = Depends(get_db)):
    return {"Added Payment Method": add_payment_method(db=db, payment_method=payment_method)}


@router.get("/payment_methods", tags=['payment_method'], status_code=201)
async def payment_methods_get(db: Session = Depends(get_db)):
    return {"Payment Methods": get_payment_methods(db=db)}