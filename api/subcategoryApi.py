import fastapi
from fastapi import Body, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.subcategoryHelpers import add_subcategory, get_subcategories

from schemas.SubcategorySchema import Subcategory as SubcategorySchema


load_dotenv(".env")
router = fastapi.APIRouter()


"""
    SUBCATEGORY ENDPOINTS
"""


@router.post("/subcategry/add/{category_id}", tags=['subcategory'], status_code=201)
async def subcategory_add(category_id: int, subcategory: SubcategorySchema, db: Session = Depends(get_db)):
    return {"Added subcategory": add_subcategory(db=db, subcategory=subcategory, category_id=category_id)}


@router.get("/subcategories", tags=['subcategory'], status_code=201)
async def subcategories_get(db: Session = Depends(get_db)):
    return {"Added subcategory": get_subcategories(db=db)}