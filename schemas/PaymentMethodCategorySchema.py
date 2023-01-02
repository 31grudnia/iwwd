from pydantic import BaseModel, Field


class PaymentMethodCategory(BaseModel):
    name: str = Field(default=None)

    class Config:
        orm_mode = True