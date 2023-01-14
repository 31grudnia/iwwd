from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    sex = Column(String(6), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    photo_url = Column(String(255), nullable=True)
    bio = Column(String(256), nullable=True)
    pins = Column(ARRAY(Integer), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="animal")
    breed_id = Column(Integer, ForeignKey("breed.id"), nullable=False)
    breed = relationship("Breed", back_populates="animal")

    pin = relationship("Pin", back_populates="animal")