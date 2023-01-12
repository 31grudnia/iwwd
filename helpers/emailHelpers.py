import os
import ssl
import smtplib
import secrets
import pytz
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from email.message import EmailMessage
from fastapi import HTTPException

from helpers.passwordHelpers import get_password_hash
from helpers.userHelpers import get_user_by_email, get_user_by_recovery_token
from schemas.PasswordRecoverySchema import PasswordRecoverySender, PasswordRecoveryReceiver

from dotenv import load_dotenv

utc=pytz.UTC
load_dotenv(".env")

EMAIL_PASSWORD="dtpvuxyigzpnwtoa"
EMAIL_SENDER="iwws.app@gmail.com"
em = EmailMessage()
em['From'] = os.environ["EMAIL_SENDER"]
em['Subject'] = "IWWD Automatic Email"


def send_test_email(email_receiver: str):
    em['To'] = email_receiver
    body = """
        IWWD Automtic Email Body
    """
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as stmp:
        stmp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        stmp.sendmail(EMAIL_SENDER, email_receiver, em.as_string())


def send_recovery_token(recovery_schema: PasswordRecoverySender, db: Session):
    check_user = get_user_by_email(db=db, email=recovery_schema.email_receiver)
    if check_user is None:
        raise HTTPException(status_code=420, detail="Email dosent exist!")

    em['To'] = recovery_schema.email_receiver
    recovery_token = secrets.token_hex(10)
    expire = datetime.utcnow() + timedelta(minutes=1)

    check_user.recovery_token = recovery_token
    check_user.recovery_token_expiration = expire
    db.commit()
    db.refresh(check_user)

    body = f"""
            Your recovery token: {recovery_token} will be valid 5 minutes.
        """
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as stmp:
        stmp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        stmp.sendmail(EMAIL_SENDER, recovery_schema.email_receiver, em.as_string())
        del em['To']
    return recovery_token


def change_user_password(recovery_schema: PasswordRecoveryReceiver, db: Session):
    if recovery_schema.new_password != recovery_schema.new_password_repeat:
        raise HTTPException(status_code=421, detail="Passwords doesnt match! (emailHelpers file)")

    db_user = get_user_by_recovery_token(db=db, token=recovery_schema.recovery_token)
    if db_user is None:
        raise HTTPException(status_code=421, detail="Recovery token is invalid! (emailHelpers file)")

    if db_user.email != recovery_schema.email_receiver:
        raise HTTPException(status_code=421, detail="Wrong email! (emailHelpers file)")

    expiration_time = db_user.recovery_token_expiration.replace(tzinfo=utc)
    now_time = datetime.utcnow().replace(tzinfo=utc)
    if now_time > expiration_time:
        raise HTTPException(status_code=421, detail="Token expired! (emailHelpers file)")

    db_user.password = get_password_hash(recovery_schema.new_password)
    db_user.recovery_token = None
    db_user.recovery_token_expiration = None
    db.commit()
    db.refresh(db_user)

    body = f"""
            Your password has been successfully changed!
        """
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as stmp:
        stmp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        stmp.sendmail(EMAIL_SENDER, recovery_schema.email_receiver, em.as_string())
        del em['To']