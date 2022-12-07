from sqlalchemy.orm import Session
from fastapi import HTTPException

from helpers.categoryHelpers import get_category

from database.models.SubcategoryModel import Subcategory as SubcategoryModel

from schemas import SubcategorySchema


def get_subcategories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SubcategoryModel).offset(skip).limit(limit).all()


def add_subcategory(db: Session, subcategory: SubcategorySchema, category_id: int):
    category_check = get_category(db=db, category_id=category_id)
    if category_check is None:
        raise HTTPException(status_code=405, detail="Category doesnt exist!")
    db_subcategory = SubcategoryModel(name=subcategory.name.title(), category_id=category_id)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory