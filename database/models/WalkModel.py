from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Time, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Walk(Base):
    __tablename__ = "walk"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time, nullable=False)
    distance = Column(Float, nullable=True)
    coins_gained = Column(Integer, nullable=False)
    start_point_latitude = Column(Float, nullable=True)
    start_point_longtitude = Column(Float, nullable=True)
    end_point_latitude = Column(Float, nullable=True)
    end_point_longtiude = Column(Float, nullable=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), onupdate=func.now())

    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False)
    animal = relationship("Animal", back_populates="walk")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # ???
    user = relationship("User", back_populates="walk")


