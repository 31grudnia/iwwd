from typing import List

from pydantic import Field, BaseModel


class PinCreate(BaseModel):
    name: str = Field(default=None)
    latitude: float = Field(default=None)
    longtitude: float = Field(default=None)
    description: str = Field(default=None)
    animal_id: int = Field(default=None)

    class Config:
        orm_mode = True