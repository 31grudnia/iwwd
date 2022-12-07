from pydantic import BaseModel, Field


class Brand(BaseModel):
    name: str = Field(default=None)
    photo: str = Field(default=None)
    description: str = Field(default=None)

    class Config:
        orm_mode = True