from pydantic import BaseModel, Field


class WalkCreate(BaseModel):


    class Config:
        orm_mode = True