from pydantic import BaseModel, Field


class Post(BaseModel):
    user_id: int = Field(default=None)
    # photo
    text: str = Field(default=None)
    likes: int = Field(default=0)
    reports: int = Field(default=0)

    class Config:
        orm_mode = True
