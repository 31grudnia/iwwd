from pydantic import BaseModel, Field, EmailStr


class MobileRegister(BaseModel):
    email: EmailStr = Field(default=None)
    login: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        orm_mode = True