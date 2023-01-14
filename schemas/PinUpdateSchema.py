from typing import List

from pydantic import Field, BaseModel


class PinUpdate(BaseModel):
    name: str = Field(default=None)
    latitude: float = Field(default=None)
    longtitude: float = Field(default=None)
    description: str = Field(default=None)

    class Config:
        orm_mode = True