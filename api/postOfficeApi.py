import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from authentication.authHandler import oauth2_scheme
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.postOfficeHelpers import get_post_office_of_user_order, get_post_office_work_time, get_post_office_by_id, \
    get_all_delivery_methods, get_post_office_with_address_by_post_office_id

load_dotenv(".env")
router = fastapi.APIRouter()

"""
    POST OFFICE ENDPOINTS
"""


@router.get("/{order_id}/post_office", tags=['post_office'], status_code=201)
async def get_post_office_of_order(order_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    post_office = await get_post_office_of_user_order(db=db, token=token, order_id=order_id)
    return {f"Post Office of order id: {order_id}": post_office}


@router.get("/post_office_work_time/{post_office_id}", tags=['post_office'], status_code=201)
async def get_wor_time_of_post_office(post_office_id: int, db: Session = Depends(get_db)):
    check_po = get_post_office_by_id(db=db, post_office_id=post_office_id)
    if check_po is None:
        raise HTTPException(status_code=469, detail=f"Post office with id: {post_office_id} doesnt exist! (postOfficeHelpers file)")
    return {f"Post Office of id: {post_office_id} work time": get_post_office_work_time(db=db, post_office_id=post_office_id)}


@router.get("/post_office/{post_office_id}", tags=['post_office'], status_code=201)
async def get_post_office(post_office_id: int, db: Session = Depends(get_db)):
    check_po = get_post_office_by_id(db=db, post_office_id=post_office_id)
    if check_po is None:
        raise HTTPException(status_code=469, detail=f"Post office with id: {post_office_id} doesnt exist! (postOfficeHelpers file)")
    return {f"Post Office of id: {post_office_id}": get_post_office_with_address_by_post_office_id(db=db, post_office_id=post_office_id)}


@router.get("/delivery_methods", tags=['delivery'], status_code=201)
async def get_delivery_methods(db: Session = Depends(get_db)):
    return {f"Delivery methods": get_all_delivery_methods(db=db)}
