from  pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    name: str = Field(default=None)
    surname: str = Field(default=None)
    city: str = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)
    phone_number: str = Field(default=None)
    login: str = Field(default=None)
    password: str = Field(default=None)
    photo: str = Field(default=None)
    regulations: int = Field(default=None)
    sex: int = Field(default=None)
    hidden_posts: int = Field(default=None)
    friends: int = Field(default=None)

    class Config:
        orm_mode = True