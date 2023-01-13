import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from database.db_generator.dbGeneratorHelpers import generate_user_records, generate_product_records,\
    generate_breeds_records


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    USER GENERATOR ENDPOINT
"""


# Insert the records into the database
@router.post("/records/users", tags=['generator'], status_code=201)
async def generator_users(n: int, db: Session = Depends(get_db)):
    generate_user_records(db=db, n=n)
    return {"message": "Records inserted successfully."}


@router.post("/records/products", tags=['generator'], status_code=201)
async def generator_products(n: int, db: Session = Depends(get_db)):
    generate_product_records(db=db, n=n)
    return {"message": "Records inserted successfully."}


@router.post("/records/breeds", tags=['generator'], status_code=201)
async def generator_breeds(db: Session = Depends(get_db)):
    generate_breeds_records(db=db)
    return {"message": "Records inserted successfully."}