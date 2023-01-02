import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session

from authentication.authHandler import oauth2_scheme
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.favouritesHelpers import add_product_to_favourites, delete_product_from_favourites


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    FAVOURITES ENDPOINTS
"""


@router.patch("/product/{product_id}/add-to-favourites", tags=['product'], status_code=201)
async def product_add_to_favourites(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    fav = await add_product_to_favourites(db=db, product_id=product_id, token=token)
    return {f"Updated product with id: {product_id}": fav}


@router.patch("/product/{product_id}/delete-from-favourites", tags=['product'], status_code=201)
async def product_delete_from_favourites(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    fav = await delete_product_from_favourites(db=db, product_id=product_id, token=token)
    return {f"Updated product with id: {product_id}": fav}