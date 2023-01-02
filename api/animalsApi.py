import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.animalHelpers import get_animals, add_animal, get_animals_with_same_user_id, update_animal_by_id, \
    delete_animal_by_id


from schemas.AnimalSchema import Animal as AnimalSchema
from schemas.AnimalUpdateSchema import UpdateAnimal as AnimalUpdateSchema

load_dotenv(".env")
router = fastapi.APIRouter()

"""
    ANIMAL ENDPOINTS
"""


@router.post("/animal/{user_id}/add", tags=['animal'], status_code=201)
async def animal_add(animal: AnimalSchema, user_id: int, db: Session = Depends(get_db)):
    return {"Added animal": add_animal(db=db, animal=animal, user_id=user_id)}


@router.get("/animals/", tags=['animal'], status_code=201)
async def animals_get(db: Session = Depends(get_db)):
    return {"All animals": get_animals(db=db)}


@router.get("/users/{user_id}/animals", tags=['animal'], status_code=201)
async def animals_get_with_same_user_id(user_id: int, db: Session = Depends(get_db)):
    return {f"Animals with user_id: {user_id}": get_animals_with_same_user_id(db=db, user_id=user_id)}


@router.patch("/animal/{animal_id}", tags=['animal'], status_code=201)
async def animal_update_by_id(animal: AnimalUpdateSchema, animal_id: int, db: Session = Depends(get_db)):
    return {f"Updated animal with id {animal_id}": update_animal_by_id(db=db, animal=animal, animal_id=animal_id)}


@router.delete("/animal/delete/{animal_id}", tags=['animal'], status_code=201)
async def animal_delete(animal_id: int, db: Session = Depends(get_db)):
    return delete_animal_by_id(db=db, animal_id=animal_id)