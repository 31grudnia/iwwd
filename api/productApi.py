import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.productHelpers import add_product, get_products, get_product_by_id, update_product_by_id, \
    delete_product_by_id

from authentication.authBearer import jwtBearer

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


@router.patch("/product/update/{product_id}", tags=['product'], status_code=201)
async def product_update(product: ProductSchema, product_id: int, db: Session = Depends(get_db)):
    return {"Updated product": update_product_by_id(db=db, product=product, product_id=product_id)}


@router.delete("/product/delete/{product_id}", tags=['product'], status_code=201)
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    return delete_product_by_id(db=db, product_id=product_id)
