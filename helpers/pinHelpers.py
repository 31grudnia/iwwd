from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from authentication.authHandler import get_current_user

from database.models.PinModel import Pin as PinModel
from helpers.animalHelpers import get_animal_by_id

from schemas.PinCreateSchema import PinCreate as PinCreateSchema
from schemas.PinUpdateSchema import PinUpdate as PinUpdateSchema


def get_pin_by_id(db: Session, index: int):
    return db.query(PinModel).filter(PinModel.id == index).first()


def get_pins_with_same_user_id(db: Session, user_id: int, animal_id: int):
    return db.query(PinModel).filter(and_(PinModel.user_id == user_id, PinModel.animal_id == animal_id)).all()


async def get_pins(db: Session, token: str, animal_id: int):
    user = await get_current_user(db=db, token=token)
    pins = get_pins_with_same_user_id(db=db, user_id=user.id, animal_id=animal_id)
    return pins


async def create_new_pin(pin: PinCreateSchema, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    check_animal = get_animal_by_id(db=db, animal_id=pin.animal_id)
    if check_animal is None:
        raise HTTPException(status_code=419, detail="Animal with this id doesnt exist! (pinHelpers file)")
    if check_animal.user_id != user.id:
        raise HTTPException(status_code=419, detail="User doesnt match with animal! (pinHelpers file)")

    db_pin = PinModel(name=pin.name, latitude=pin.latitude, longtitude=pin.longtitude, description=pin.description,
                      user_id=user.id, animal_id=pin.animal_id)
    db.add(db_pin)
    db.commit()
    db.refresh(db_pin)
    return {"Created walk": db_pin}


async def delete_pin(pin_id: int, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    check_pin = get_pin_by_id(db=db, index=pin_id)
    if check_pin is None:
        raise HTTPException(status_code=419, detail=f"Pin with id: {pin_id} doesnt exist! (pinHelpers file)")

    if check_pin.user_id != user.id:
        raise HTTPException(status_code=419, detail=f"Pin with id: {pin_id} doesnt belong to currently logged in "
                                                    f"user! (pinHelpers file)")

    db.delete(check_pin)
    db.commit()
    return {"message": "Record successfully deleted"}


async def update_pin(pin_id: int, pin: PinUpdateSchema, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    check_pin = get_pin_by_id(db=db, index=pin_id)
    if check_pin is None:
        raise HTTPException(status_code=419, detail=f"Pin with id: {pin_id} doesnt exist! (pinHelpers file)")

    if check_pin.user_id != user.id:
        raise HTTPException(status_code=419, detail=f"Pin with id: {pin_id} doesnt belong to currently logged in "
                                                    f"user! (pinHelpers file)")

    check_pin.name = pin.name
    check_pin.description = pin.description
    check_pin.latitude = pin.latitude
    check_pin.longtitude = pin.longtitude

    db.commit()
    db.refresh(check_pin)
    return check_pin