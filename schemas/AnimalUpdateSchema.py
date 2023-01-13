from datetime import date

from pydantic import BaseModel, Field


class UpdateAnimal(BaseModel):
    name: str = Field(default=None)
    weight: float = Field(default=None)
    height: float = Field(default=None)
    bio: str = Field(default=None)

    class Config:
        orm_mode = True