import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv
from authentication.authHandler import oauth2_scheme

from helpers.pinHelpers import create_new_pin, delete_pin, update_pin, get_pins, get_pins_with_same_user_id

from schemas.PinUpdateSchema import PinUpdate as PinUpdateSchema
from schemas.PinCreateSchema import PinCreate as PinCreateSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    PIN ENDPOINTS
"""


@router.get("/pins/{animal_id}", tags=['pin'], status_code=201)
async def pins_get_of_current_user(animal_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    pins = await get_pins(db=db, token=token, animal_id=animal_id)
    return {"pins": pins}


@router.get("/pins/{user_id}/{animal_id}", tags=['pin'], status_code=201)
async def pins_get_of_current_user(animal_id: int, user_id: int, db: Session = Depends(get_db)):
    pins = get_pins_with_same_user_id(db=db, animal_id=animal_id, user_id=user_id)
    return {"pins": pins}


@router.post("/pin/add", tags=['pin'], status_code=201)
async def pin_add(pin: PinCreateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    pin = await create_new_pin(pin=pin, db=db, token=token)
    return {"Added pin": pin}


@router.delete("/pin/delete/{pin_id}", tags=['pin'], status_code=201)
async def pin_delete(pin_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    pin = await delete_pin(pin_id=pin_id, db=db, token=token)
    return {"Deleted pin": pin}


@router.patch("/pin/update/{pin_id}", tags=['pin'], status_code=201)
async def pin_update(pin_id: int, pin: PinUpdateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    pin = await update_pin(pin_id=pin_id, pin=pin, db=db, token=token)
    return {"Updated pin": pin}