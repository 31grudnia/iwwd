from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Breed(Base):
    __tablename__ = "breed"

    id = Column(Integer, primary_key=True, index=True)
    dog_breed = Column(String(30), nullable=True)
    cat_breed = Column(String(30), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal = relationship("Animal", back_populates="breed")

    