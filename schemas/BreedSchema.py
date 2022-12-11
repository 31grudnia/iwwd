from pydantic import BaseModel, Field


class Breed(BaseModel):
    dog_breed: str = Field(default=None)
    cat_breed: str = Field(default=None)

    class Config:
        orm_mode = True