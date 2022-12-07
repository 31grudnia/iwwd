import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.productHelpers import add_product, get_products, get_product_by_id

from schemas.ProductSchema import Product as ProductSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    PRODUCT ENDPOINTS
"""


@router.post("/product/add", tags=['product'], status_code=201)
async def product_add(product: ProductSchema, db: Session = Depends(get_db)):
    return {"Added product": add_product(db=db, product=product)}


@router.get("/products", tags=['product'], status_code=201)
async def products_get(db: Session = Depends(get_db)):
    return {"All products": get_products(db=db)}


@router.get("/product/{product_id}", tags=['product'], status_code=201)
async def product_get(product_id: int, db: Session = Depends(get_db)):
    return {"Product": get_product_by_id(db=db, index=product_id)}