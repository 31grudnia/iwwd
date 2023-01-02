from pydantic import BaseModel, Field


class PaymentMethod(BaseModel):
    name: str = Field(default=None)
    photo: str = Field(default=None)
    payment_method_category_id: int = Field(default=None)

    class Config:
        orm_mode = True