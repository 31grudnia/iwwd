from sqlalchemy import Column, DateTime, ForeignKey, String, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database.db_setup import Base

class BreedDog(enum.Enum):
    breed_dog_small_1 = 1
    breed_dog_medium_2 = 2
    breed_dog_big_3 = 3
    breed_dog_other_4 = 4

class BreedCat(enum.Enum):
    breed_cat_small_1 = 1
    breed_cat_medium_2 = 2
    breed_cat_big_3 = 3
    breed_cat_other_4 = 4

class Breed(Base):
    __tablename__ = "breed"

    id = Column(Integer, primary_key=True, index=True)
    dog_breed = Column(Enum(BreedDog), nullable=True)
    cat_breed = Column(Enum(BreedCat), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal = relationship("Animal", back_populates="breed")

    