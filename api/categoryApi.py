import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.categoryHelpers import add_category, get_categories, get_categories_with_subs

from schemas.CategorySchema import Category as CategorySchema


load_dotenv(".env")
router = fastapi.APIRouter()


"""
    CATEGORY ENDPOINTS
"""


@router.post("/categry/add", tags=['category'], status_code=201)
async def category_add(category: CategorySchema, db: Session = Depends(get_db)):
    return {"Added category": add_category(db=db, category=category)}


@router.get("/categories", tags=['category'], status_code=201)
async def categories_get(db: Session = Depends(get_db)):
    return {"Categories": get_categories(db=db)}


@router.get("/categories/subcategories", tags=['category'], status_code=201)    # OK???
async def cetegories_with_subs_get(db: Session = Depends(get_db)):
    return {'Categories with subcategoriess': get_categories_with_subs(db=db)}