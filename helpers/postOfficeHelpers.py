from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from authentication.authHandler import get_current_user
from database.models.PostOfficeModel import PostOffice as PostOfficeModel
from database.models.PostOfficeAddressModel import PostOfficeAddress as PostOfficeAddressModel
from database.models.PostOfficeWorkTimeModel import PostOfficeWorkTime as PostOfficeWorkTimeModel
from database.models.DeliveryMethodModel import DeliveryMethod as DeliveryMethodModel
from helpers.orderHelpers import get_order_by_id



def get_post_office_by_id(db: Session, post_office_id: int):
    return db.query(PostOfficeModel).filter(PostOfficeModel.id == post_office_id).first()


def get_post_office_with_address_by_order_id(db: Session, order_id: int):
    subquery = select([PostOfficeModel.id]).where(PostOfficeModel.order_id == order_id)
    query = db.query(PostOfficeModel, PostOfficeAddressModel)\
        .outerjoin(PostOfficeAddressModel, PostOfficeModel.post_office_address_id ==
                   PostOfficeAddressModel.id).filter(PostOfficeModel.id.in_(subquery)).all()
    return query


def get_post_office_with_address_by_post_office_id(db: Session, post_office_id: int):
    subquery = select([PostOfficeModel.id]).where(PostOfficeModel.id == post_office_id)
    query = db.query(PostOfficeModel, PostOfficeAddressModel)\
        .outerjoin(PostOfficeAddressModel, PostOfficeModel.post_office_address_id ==
                   PostOfficeAddressModel.id).filter(PostOfficeModel.id.in_(subquery)).all()
    return query


def get_post_office_by_order_id(db: Session, order_id: int):
    return db.query(PostOfficeModel).filter(PostOfficeModel.order_id == order_id).first()


def get_post_office_work_time(db: Session, post_office_id: int):
    return db.query(PostOfficeWorkTimeModel).filter(PostOfficeWorkTimeModel.post_office_id == post_office_id).all()


def get_all_delivery_methods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeliveryMethodModel).offset(skip).limit(limit).all()


async def get_post_office_of_user_order(order_id: int, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    check_order = get_order_by_id(db=db, index=order_id)
    if check_order.user_id != user.id:
        raise HTTPException(status_code=469, detail=f"Order with id: {order_id} doesnt belong to currently logged in "
                                                    f"user! (postOfficeHelpers file)")

    post_office = get_post_office_with_address_by_order_id(db=db, order_id=order_id)
    return post_office
