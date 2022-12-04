import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from schemas.ProductSchema import Product as ProductSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    PRODUCT ENDPOINTS
"""

@router.post("/product", tags=['user'], status_code=201)
async def user_register_web(product: ProductSchema, db: Session = Depends(get_db)):
    pass