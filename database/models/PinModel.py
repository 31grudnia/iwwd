from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base

class Pin(Base):
    __tablename__ = "pin"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=True)
    longtitude = Column(Float, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False)
    animal = relationship("Animal", back_populates="post")