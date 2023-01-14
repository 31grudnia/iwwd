from sqlalchemy.orm import Session
from fastapi import HTTPException

from authentication.authHandler import get_current_user
from helpers.animalHelpers import get_animal_by_id
from helpers.userHelpers import get_user_by_id

from database.models.WalkModel import Walk as WalkModel

from schemas.WalkCreateSchema import WalkCreate as WalkCreateSchema


def get_walk_by_id(db: Session, index: int):
    return db.query(WalkModel).filter(WalkModel.id == index).first()


def get_walks_with_same_user_id(db: Session, user_id: int):
    return db.query(WalkModel).filter(WalkModel.user_id == user_id).all()


async def get_walks(db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    walks = get_walks_with_same_user_id(db=db, user_id=user.id)
    return walks


async def create_new_walk(walk: WalkCreateSchema, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    db_user = get_user_by_id(index=user.id, db=db)
    for i in walk.animals_id:
        check_animal = get_animal_by_id(animal_id=i, db=db)
        if check_animal is None:
            raise HTTPException(status_code=419, detail=f"Animal with id: {i} doesnt exist! (walkHelpers file)")
        if check_animal.user_id != db_user.id:
            raise HTTPException(status_code=419, detail=f"Animal with id: {i} doesnt belong to currently logged in "
                                                        f"user! (walkHelpers file)")

    db_walk = WalkModel(time=walk.time, distance=walk.distance, coins_gained=walk.coins_gained,
                        animals_id=walk.animals_id, user_id=user.id, photo=walk.photo)
    db_user.coins = db_user.coins + walk.coins_gained
    db.add(db_walk)
    db.commit()
    db.refresh(db_walk)
    return {"Created walk": db_walk}


async def delete_walk(walk_id: int, db: Session, token: str):
    user = await get_current_user(db=db, token=token)
    check_walk = get_walk_by_id(db=db, index=walk_id)
    if check_walk is None:
        raise HTTPException(status_code=419, detail=f"Walk with id: {walk_id} doesnt exist! (walkHelpers file)")

    if check_walk.user_id != user.id:
        raise HTTPException(status_code=419, detail=f"Walk with id: {walk_id} doesnt belong to currently logged in "
                                                    f"user! (walkHelpers file)")

    db.delete(check_walk)
    db.commit()
    return {"message": "Record successfully deleted"}