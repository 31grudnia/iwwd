from pydantic import BaseModel, Field, EmailStr


class Register(BaseModel):
    name: str = Field(default=None)
    surname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    phone_number: str = Field(default=None)

    state: str = Field(default=None)
    city: str = Field(default=None)
    home_number: str = Field(default=None)
    post_code: str = Field(default=None)
    street: str = Field(default=None)

    login: str = Field(default=None)
    password: str = Field(default=None)
    password_repeat: str = Field(default=None)

    class Config:
        orm_mode = True