import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.brandHelpers import add_brand, get_brands

from schemas.BrandSchema import Brand as BrandSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    BRAND ENDPOINTS
"""


@router.post("/brand/add", tags=['brand'], status_code=201)
async def brand_add(brand: BrandSchema, db: Session = Depends(get_db)):
    return {"Added brand": add_brand(db=db, brand=brand)}


@router.get("/brands", tags=['brand'], status_code=201)
async def brands_get(db: Session = Depends(get_db)):
    return {"All brands": get_brands(db=db)}
