from sqlalchemy.orm import Session
from fastapi import HTTPException

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

    check_brand = get_brand_by_id(db=db, index=product.brand_id)
    if check_brand is None:
        raise HTTPException(status_code=406, detail="Brand doesnt exist! (productHelpers file)")

    db_product = ProductModel(title=product.title.title(), short_description=product.short_description,
                              long_description=product.long_description,
                              price=calculate_product_price(base_price=product.base_price,
                                                            discount_price=product.discount_price,
                                                            discount_amount=product.discount_amount),
                              base_price=product.base_price, discount_price=product.discount_price,
                              discount_amount=product.discount_amount,
                              rate=product.rate, ingredients=product.ingredients, dosage=product.dosage,
                              favourite=product.favourite,
                              subcategory_id=product.subcategory_id, brand_id=product.brand_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product_by_id(db: Session, product: ProductSchema, product_id: int):
    check_product = get_product_by_id(db=db, index=product_id)
    if check_product is None:
        raise HTTPException(status_code=406, detail="Product doesnt exist! (productHelpers file)")

    check_subcategory = get_subcategory_by_id(db=db, index=product.subcategory_id)
    if check_subcategory is None:
        raise HTTPException(status_code=406, detail="Subcategory doesnt exist! (productHelpers file)")

    check_brand = get_brand_by_id(db=db, index=product.brand_id)
    if check_brand is None:
        raise HTTPException(status_code=406, detail="Brand doesnt exist! (productHelpers file)")

    check_product.title = product.title.title()
    check_product.short_description = product.short_description
    check_product.long_description = product.long_description
    check_product.price = calculate_product_price(base_price=product.base_price, discount_price=product.discount_price,
                                                  discount_amount=product.discount_amount)
    check_product.base_price = product.base_price
    check_product.discount_price = product.discount_price
    check_product.discount_amount = product.discount_amount
    check_product.rate = product.rate
    check_product.ingredients = product.ingredients
    check_product.dosage = product.dosage
    check_product.favourite = product.favourite
    check_product.subcategory_id = product.subcategory_id
    check_product.brand_id = product.brand_id

    db.commit()
    db.refresh(check_product)
    return check_product


def delete_product_by_id(db: Session, product_id: int):
    check_product = get_product_by_id(db=db, index=product_id)
    if check_product is None:
        raise HTTPException(status_code=406, detail="Product doesnt exist! (productHelpers file)")
    db.delete(check_product)
    db.commit()
    return {"message": "Record successfully deleted"}


def calculate_product_price(base_price: float, discount_price: float, discount_amount: int):
    return base_price - discount_price * discount_amount


