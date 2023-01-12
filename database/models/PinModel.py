from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Pin(Base):
    __tablename__ = "pin"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=False)
    longtitude = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False)
    animal = relationship("Animal", back_populates="pin")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="pin")
