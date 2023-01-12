import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db_setup import get_db
from dotenv import load_dotenv

from helpers.emailHelpers import send_recovery_token, change_user_password
from schemas.PasswordRecoverySchema import PasswordRecoverySender, PasswordRecoveryReceiver

load_dotenv(".env")
router = fastapi.APIRouter()


@router.post("/user/recovery_password", tags=['email'], status_code=201)
async def user_recovery_password(recovery_schema: PasswordRecoverySender, db: Session = Depends(get_db)):
    return {"Email send": send_recovery_token(db=db, recovery_schema=recovery_schema)}


@router.post("/user/password_recovery_page", tags=['email'], status_code=201)
async def user_password_recovery_page(recovery_schema: PasswordRecoveryReceiver, db: Session = Depends(get_db)):
    return {"New password": change_user_password(db=db, recovery_schema=recovery_schema)}