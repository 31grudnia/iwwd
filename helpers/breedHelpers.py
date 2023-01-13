from sqlalchemy.orm import Session

from database.models.BreedModel import Breed as BreedModel


def get_breeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BreedModel).offset(skip).limit(limit).all()


def get_breed_by_id(db: Session, index: int):
    return db.query(BreedModel).filter(BreedModel.id == index).first()


