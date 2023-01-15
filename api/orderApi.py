import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from authentication.authHandler import oauth2_scheme
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.orderHelpers import create_new_order, get_my_orders
from schemas.OrderCreateSchema import OrderCreate as OrderCreateSchema

load_dotenv(".env")
router = fastapi.APIRouter()

"""
    ORDER ENDPOINTS
"""


@router.get("/orders/me", tags=['order'], status_code=201)
async def orders_me_get(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    orders = await get_my_orders(db=db, token=token)
    return {f"Your orders": orders}


@router.post("/order/create", tags=['order'], status_code=201)
async def order_add(order: OrderCreateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    order = await create_new_order(db=db, order=order, token=token)
    return {"Created order": order}

