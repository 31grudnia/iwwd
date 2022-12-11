from datetime import date
from pydantic import Field

from schemas.AnimalUpdateSchema import UpdateAnimal


class Animal(UpdateAnimal):
    # name: str = Field(default=None)
    sex: str = Field(default=None)
    kind: str = Field(default=None)
    # weight: float = Field(default=None)
    # height: float = Field(default=None)
    # photo: str = Field(default=None)
    # bio: str = Field(default=None)
    # pins: int = Field(default=None)
    birth_date: date = Field(default=None)
    breed_id: int = Field(default=None)