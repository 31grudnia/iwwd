from  pydantic import BaseModel, Field

class Walk(BaseModel):
    user_id: int = Field(default=None)
    distance: float = Field(default=None)
    coins_gained: int = Field(default=0)
    route_match: bool = Field(default=False)
    start_point_latitude: float = Field(default=None)
    start_point_longtitude: float = Field(default=None)
    end_point_latitude: float = Field(default=None)
    end_point_longtiude: float = Field(default=None)
    places: str = Field(default=None)
    route_type: str = Field(default='straight')