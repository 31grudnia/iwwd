from pydantic import Field, BaseModel


class UserUpdatePassword(BaseModel):
    old_password: str = Field(default=None)
    new_password: str = Field(default=None)

    class Config:
        orm_mode = True