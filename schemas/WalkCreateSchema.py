from typing import List

from pydantic import Field, BaseModel


class WalkCreate(BaseModel):
    time: str = Field(default=None)
    distance: float = Field(default=None)
    coins_gained: int = Field(default=None)
    animals_id: List[int] = Field(default=[])
    photo: List[int] = Field(default=[])

    class Config:
        orm_mode = True