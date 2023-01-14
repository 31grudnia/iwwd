import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv
from authentication.authHandler import oauth2_scheme

from helpers.walkHelpers import create_new_walk, delete_walk, get_walks

from schemas.WalkCreateSchema import WalkCreate as WalkCreateSchema


load_dotenv(".env")
router = fastapi.APIRouter()

"""
    WALK ENDPOINTS
"""


@router.get("/walks", tags=['walk'], status_code=201)
async def walks_get(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    walks = await get_walks(db=db, token=token)
    return {"Walks": walks}


@router.post("/walk/add", tags=['walk'], status_code=201)
async def walk_add(walk: WalkCreateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    walk = await create_new_walk(walk=walk, db=db, token=token)
    return {"Added walk": walk}


@router.delete("/walk/delete/{walk_id}", tags=['walk'], status_code=201)
async def walk_delete(walk_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    walk = await delete_walk(walk_id=walk_id, db=db, token=token)
    return {"Deleted walk": walk}