import numpy as np
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import HTTPException

from authentication.authHandler import get_current_user
from helpers.productHelpers import get_product_by_id
from helpers.userHelpers import get_user_by_id

load_dotenv(".env")


async def add_product_to_favourites(product_id: int, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    db_user = get_user_by_id(db=db, index=user.id)
    check_product = get_product_by_id(db=db, index=product_id)
    if check_product is None:
        raise HTTPException(status_code=419,
                            detail=f"Product with id: {product_id} doesnt exist (favouriteHelpers file)")

    if product_id in db_user.favourites:
        raise HTTPException(status_code=419, detail="Product is already favourite (favouriteHelpers file)")
    else:
        db_user.favourites = db_user.favourites + [product_id]
        db.commit()
        db.refresh(db_user)
        return {f"Record with id: {product_id} added successfully to favourites!": db_user.favourites}


async def delete_product_from_favourites(product_id: int, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    db_user = get_user_by_id(db=db, index=user.id)
    check_product = get_product_by_id(db=db, index=product_id)
    if check_product is None:
        raise HTTPException(status_code=419, detail=f"Product with id: {product_id} doesnt exist (favouriteHelpers file)")

    if product_id in db_user.favourites:
        arr = np.array(db_user.favourites)
        product_index = np.where(arr == product_id)
        arr = np.delete(arr, product_index)
        db_user.favourites = arr.astype(list)
        db.commit()
        db.refresh(db_user)
        return {f"Record with id: {product_id} removed successfully!": db_user.favourites, "new tab": "new_tab"}
    else:
        raise HTTPException(status_code=419, detail="Product is not favourite (favouriteHelpers file)")