from sqlalchemy.orm import Session
from sqlalchemy import select, join, exists
from fastapi import HTTPException

from authentication.authHandler import get_current_user
from database.db_generator.dbGeneratorHelpers import fake
from helpers.paymentMethodHelpers import get_payment_method_by_id
from helpers.productHelpers import get_product_by_id
from helpers.statusHelpers import get_status_by_id

from schemas.OrderCreateSchema import OrderCreate as OrderCreateSchema

from database.models.OrderModel import Order as OrderModel
from database.models.OrderProductModel import OrderProduct as OrderProductModel


def get_orders_with_products_by_user_id(db: Session, user_id: int):
    subquery = select([OrderModel.id]).where(OrderModel.user_id == user_id)
    query = db.query(OrderModel, OrderProductModel)\
        .outerjoin(OrderProductModel, OrderModel.id == OrderProductModel.order_id).filter(OrderModel.id.in_(subquery)).all()
    return query


async def get_my_orders(db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    return get_orders_with_products_by_user_id(db=db, user_id=user.id)


async def create_new_order(order: OrderCreateSchema, db: Session, token: str):
    if len(order.products_id) != len(order.amounts_of_products):
        raise HTTPException(status_code=469, detail=f"Wrong given amount of products! (orderHelpers file)")

    for i in range(len(order.products_id)):
        check_product = get_product_by_id(db=db, index=order.products_id[i])
        if check_product is None:
            raise HTTPException(status_code=469, detail=f"Product with id: {i} doesnt exist! (orderHelpers file)")
        if check_product.amount < order.amounts_of_products[i]:
            raise HTTPException(status_code=469, detail=f"Not enough products of id: {check_product.id} in storge!"
                                                        f" (orderHelpers file)")
        else:
            check_product.amount = check_product.amount - order.amounts_of_products[i]

    check_payment_method = get_payment_method_by_id(db=db, index=order.payment_method_id)
    if check_payment_method is None:
        raise HTTPException(status_code=469, detail=f"Payment method with id: {id} doesnt exist! (orderHelpers file)")
    check_status = get_status_by_id(db=db, index=order.status_id)
    if check_status is None:
        raise HTTPException(status_code=469, detail=f"Status with id: {id} doesnt exist! (orderHelpers file)")

    user = await get_current_user(db=db, token=token)
    db_order = OrderModel(order_code=fake.isbn13(), city=order.city.title(), street=order.street.title(),
                          home_number=order.home_number, post_code=order.post_code, status_id=order.status_id,
                          payment_method_id=order.payment_method_id, user_id=user.id)
    db.add(db_order)
    db.commit()

    for i in range(len(order.products_id)):
        db_order_product = OrderProductModel(order_id=db_order.id,
                                             product_id=order.products_id[i], amount=order.amounts_of_products[i])
        db.add(db_order_product)

    db.commit()
    return {"Order created": "successful"}