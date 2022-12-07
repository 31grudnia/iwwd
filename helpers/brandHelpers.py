from sqlalchemy.orm import Session
from fastapi import Body, HTTPException

from database.models.BrandModel import Brand as BrandModel

from schemas import BrandSchema

def get_brand_by_id(db: Session, index: int):
    return db.query(BrandModel).filter(BrandModel.id == index).first()


def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BrandModel).offset(skip).limit(limit).all()


def get_brand_by_name(db: Session, name: str):
    return db.query(BrandModel).filter(BrandModel.name == name.title()).first()


def add_brand(db: Session, brand: BrandSchema):
    check_brand = get_brand_by_name(db=db, name=brand.name)
    if check_brand:
        raise HTTPException(status_code=406, detail="Brand already exists! (brandHelpers file)")

    db_brand = BrandModel(name=brand.name.title(), photo=brand.photo, description=brand.description)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand