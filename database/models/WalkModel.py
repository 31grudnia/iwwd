from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Enum, Time, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database.db_setup import Base

class WalkRouteType(enum.Enum):
    straight = 1
    loop = 2

class WalkPlaces(enum.Enum):
    shop = 1
    vet = 2
    park = 3
    restaurant = 4

class Walk(Base):
    __tablename__ = "walk"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time, nullable=False)
    distance = Column(Float, nullable=True)
    coins_gained = Column(Integer, nullable=False)
    time_limit = Column(Time, nullable=True)
    route_match = Column(Boolean, nullable=True)
    start_point_latitude = Column(Float, nullable=True)
    start_point_longtitude = Column(Float, nullable=True)
    end_point_latitude = Column(Float, nullable=True)
    end_point_longtiude = Column(Float, nullable=True)
    places = Column(Enum(WalkPlaces), nullable=True)
    route_type = Column(Enum(WalkRouteType), nullable=False)
    #animal_list = Column()
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="walk")

