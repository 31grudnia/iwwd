from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str = Field(default=None)

    class Config:
        orm_mode = True