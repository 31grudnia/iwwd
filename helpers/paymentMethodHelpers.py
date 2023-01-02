from sqlalchemy.orm import Session
from fastapi import HTTPException

from helpers.paymentMethodCategoryHelpers import get_payment_method_category_by_id

from database.models.PaymentMethodModel import PaymentMethod as PaymentMethodModel

from schemas import PaymentMethodSchema


def get_payment_method_by_id(db: Session, index: int):
    return db.query(PaymentMethodModel).filter(PaymentMethodModel.id == index).first()


def get_payment_method_by_name(db: Session, name: str):
    return db.query(PaymentMethodModel).filter(PaymentMethodModel.name == name.title()).first()


def get_payment_methods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PaymentMethodModel).offset(skip).limit(limit).all()


def add_payment_method(db: Session, payment_method: PaymentMethodSchema):
    pmcategory_check = get_payment_method_category_by_id(db=db, index=payment_method.payment_method_category_id)
    if pmcategory_check is None:
        raise HTTPException(status_code=411, detail="Payment Method Category doesnt exist!")

    pm_check = get_payment_method_by_name(db=db, name=payment_method.name)
    if pm_check is None:
        raise HTTPException(status_code=411, detail="Payment Method already exists!")

    db_payment_method = PaymentMethodModel(name=payment_method.name.title(), photo=payment_method.photo,
                                           payment_method_category_id=payment_method.payment_method_category_id)
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method