from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models.CategoryModel import Category as CategoryModel
from database.models.SubcategoryModel import Subcategory as SubcategoryModel


from schemas import CategorySchema


def get_category(db: Session, category_id: int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CategoryModel).offset(skip).limit(limit).all()


def get_categories_with_subs(db: Session):
    return db.query(CategoryModel, SubcategoryModel).filter(CategoryModel.id == SubcategoryModel.category_id).all()


def get_category_by_name(db: Session, name: str):
    return db.query(CategoryModel).filter(CategoryModel.name == name).first()


def add_category(db: Session, category: CategorySchema):
    category_check = get_category_by_name(db=db, name=category.name.title())
    if category_check:
        raise HTTPException(status_code=404, detail="Category already exists!")
    db_category = CategoryModel(name=category.name.title())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


