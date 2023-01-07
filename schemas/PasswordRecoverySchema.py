from pydantic import BaseModel, Field, EmailStr


class PasswordRecoverySender(BaseModel):
    email_receiver: EmailStr = Field(default=None)


class PasswordRecoveryReceiver(PasswordRecoverySender):
    recovery_token: str
    new_password: str
    new_password_repeat: str