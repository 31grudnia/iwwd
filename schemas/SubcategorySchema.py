from pydantic import BaseModel, Field


class Subcategory(BaseModel):
    name: str = Field(default=None)

    class Config:
        orm_mode = True