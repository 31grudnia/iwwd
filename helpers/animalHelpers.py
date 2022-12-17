from sqlalchemy.orm import Session
from fastapi import HTTPException

from helpers.userHelpers import get_user_by_id
from helpers.breedHelpers import get_breed_by_id

from database.models.AnimalModel import Animal as AnimalModel

from schemas import AnimalSchema, AnimalUpdateSchema


def get_animals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AnimalModel).offset(skip).limit(limit).all()


def get_animal_by_id(db: Session, animal_id: int):
    return db.query(AnimalModel).filter(AnimalModel.id == animal_id).first()


def get_animals_with_same_user_id(db: Session, user_id: int):
    return db.query(AnimalModel).filter(AnimalModel.user_id == user_id).all()


def add_animal(db: Session, animal: AnimalSchema, user_id: int):
    check_user = get_user_by_id(db=db, index=user_id)
    if check_user is None:
        raise HTTPException(status_code=409, detail="User doesnt exist! (animalHelpers file)")

    check_breed = get_breed_by_id(db=db, index=animal.breed_id)
    if check_breed is None:
        raise HTTPException(status_code=409, detail="Breed doesnt exist! (animalHelpers file)")

    db_animal = AnimalModel(name=animal.name.title(), sex=animal.sex.title(), kind=animal.kind.title(),
                            weight=animal.weight, height=animal.height,
                            photo=animal.photo, bio=animal.bio, pins=animal.pins,
                            user_id=user_id, breed_id=animal.breed_id, birth_date=animal.birth_date)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def update_animal_by_id(db: Session, animal: AnimalUpdateSchema, animal_id: int):
    check_animal = get_animal_by_id(db=db, animal_id=animal_id)
    if check_animal is None:
        raise HTTPException(status_code=409, detail="Animal doesnt exist! (animalHelpers file)")

    check_animal.name = animal.name.title()
    check_animal.weight = animal.weight
    check_animal.height = animal.height
    check_animal.photo = animal.photo
    check_animal.bio = animal.bio
    check_animal.pins = animal.pins

    db.commit()
    db.refresh(check_animal)
    return check_animal


def delete_animal_by_id(db: Session, animal_id: int):
    check_animal = get_animal_by_id(db=db, animal_id=animal_id)
    if check_animal is None:
        raise HTTPException(status_code=406, detail="Animal doesnt exist! (animalHelpers file)")
    db.delete(check_animal)
    db.commit()
    return {"message": "Record successfully deleted"}