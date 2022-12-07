from  pydantic import BaseModel, Field, EmailStr


class Login(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        orm_mode = True