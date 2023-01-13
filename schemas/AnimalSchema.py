from pydantic import BaseModel, Field


class Animal(BaseModel):
    name: str = Field(default=None)
    birth_date: str = Field(default=None)
    sex: str = Field(default=None)
    weight: float = Field(default=None)
    height: float = Field(default=None)
    bio: str = Field(default=None)
    breed_id: int = Field(default=None)

    class Config:
        orm_mode = True