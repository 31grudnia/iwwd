from sqlalchemy.orm import Session
from fastapi import Body, HTTPException
from fastapi.encoders import jsonable_encoder

from database.models.AddressModel import Address as AddressModel
from database.models.UserModel import User as UserModel

from schemas import RegisterWebSchema


def get_address_by_id(db: Session, index: int):
    return db.query(AddressModel).filter(AddressModel.id == index).first()


def add_address_by_web(db: Session, register: RegisterWebSchema, user: UserModel):
    db_address = AddressModel(state=register.state.title(), city=register.city.title(), street=register.street.title(),
                              home_number=register.home_number, post_code=register.post_code, user_id=user.id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address






