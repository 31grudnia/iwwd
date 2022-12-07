from sqlalchemy.orm import Session
from fastapi import Body, HTTPException

from helpers.subcategoryHelpers import get_subcategory_by_id
from helpers.brandHelpers import get_brand_by_id

from database.models.ProductModel import Product as ProductModel

from schemas import ProductSchema


def get_product_by_id(db: Session, index: int):
    return db.query(ProductModel).filter(ProductModel.id == index).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductModel).offset(skip).limit(limit).all()


def get_product_by_name(db: Session, title: str):
    return db.query(ProductModel).filter(ProductModel.title == title.title()).first()


def add_product(db: Session, product: ProductSchema):
    check_product = get_product_by_name(db=db, title=product.title)
    if check_product:
        raise HTTPException(status_code=406, detail="Product already exists! (productHelpers file)")

    check_subcategory = get_subcategory_by_id(db=db, index=product.subcategory_id)
    if check_subcategory is None:
        raise HTTPException(status_code=406, detail="Subcategory doesnt exist! (productHelpers file)")

    check_brand = get_brand_by_id(db=db, index=product.subcategory_id)
    if check_brand is None:
        raise HTTPException(status_code=406, detail="Brand doesnt exist! (productHelpers file)")

    db_product = ProductModel(title=product.title.title(), short_description=product.short_description, long_description=product.long_description,
                              price=product.price, base_price=product.base_price, discount_price=product.discount_price, discount_amount=product.discount_amount,
                              rate=product.rate, ingredients=product.ingredients, dosage=product.dosage, favourite=product.favourite,
                              subcategory_id=product.subcategory_id, brand_id=product.brand_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# def for counting prrice