from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username_email: str | None = None

    class Config:
        orm_mode = True

