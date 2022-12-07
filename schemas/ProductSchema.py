from pydantic import BaseModel, Field


class Product(BaseModel):
    title: str = Field(default=None)
    short_description: str = Field(default=None)
    long_description: str = Field(default=None)
    price: float = Field(default=None)
    base_price: float = Field(default=None)
    discount_price: float
    discount_amount: int
    rate: int = Field(default=0)
    ingredients: str = Field(default=None)
    dosage: str = Field(default=None)
    favourite: bool = Field(default=False)

    class Config:
        orm_mode = True