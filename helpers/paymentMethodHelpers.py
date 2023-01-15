from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models.PaymentMethodModel import PaymentMethod as PaymentMethodModel


def get_payment_method_by_id(db: Session, index: int):
    return db.query(PaymentMethodModel).filter(PaymentMethodModel.id == index).first()


def get_payment_method_by_name(db: Session, name: str):
    return db.query(PaymentMethodModel).filter(PaymentMethodModel.name == name.title()).first()


def get_payment_methods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PaymentMethodModel).offset(skip).limit(limit).all()
