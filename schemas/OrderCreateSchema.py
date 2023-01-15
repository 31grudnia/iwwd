from pydantic import Field, BaseModel
from typing import List


class OrderCreate(BaseModel):
    city: str = Field(default=None)
    street: str = Field(default=None)
    home_number: str = Field(default=None)
    post_code: str = Field(default=None)

    status_id: int = Field(default=1)
    payment_method_id: int = Field(default=None)

    products_id: List[int] = Field(default=[])
    amounts_of_products: List[int] = Field(default=[])

    class Config:
        orm_mode = True