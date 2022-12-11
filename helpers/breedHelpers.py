from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models.BreedModel import Breed as BreedModel

from schemas import BreedSchema


def get_breeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BreedModel).offset(skip).limit(limit).all()


def get_breed_by_id(db: Session, index: int):
    return db.query(BreedModel).filter(BreedModel.id == index).first()


def get_breed_by_dog(db: Session, name: str):
    return db.query(BreedModel).filter(BreedModel.dog_breed == name.title()).first()


def get_breed_by_cat(db: Session, name: str):
    return db.query(BreedModel).filter(BreedModel.cat_breed == name.title()).first()


def add_breed(db: Session, breed: BreedSchema):
    check_breed = get_breed_by_dog(db=db, name=breed.dog_breed)
    if check_breed and check_breed.dog_breed != "":
        raise HTTPException(status_code=408, detail="Dog Breed already exists! (breedHelpers file)")

    check_breed = get_breed_by_cat(db=db, name=breed.cat_breed)
    if check_breed and check_breed.cat_breed != "":
        raise HTTPException(status_code=408, detail="Cat Breed already exists! (breedHelpers file)")

    check_breeds(breed=breed)
    db_breed = BreedModel(dog_breed=breed.dog_breed.title(), cat_breed=breed.cat_breed.title())
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed


def check_breeds(breed: BreedSchema):
    if breed.dog_breed is None and breed.cat_breed is None:
        raise HTTPException(status_code=408, detail="Cannot add None as both breeds! (breedHelpers file)")