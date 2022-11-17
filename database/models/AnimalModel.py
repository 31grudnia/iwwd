from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Float, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database.db_setup import Base

class AnimalSex(enum.Enum):
    male = 1
    female = 2

class AnimalKind(enum.Enum):
    dog = 1
    cat = 2

class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    birth_date = Column(Date, nullable=True)
    sex = Column(Enum(AnimalSex))
    kind = Column(Enum(AnimalKind))
    weight = Column(Float)
    height = Column(Float)
    photo = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    pins = Column(Integer, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="animal")
    breed_id = Column(Integer, ForeignKey("breed.id"), nullable=False)
    breed = relationship("Breed", back_populates="animal")
    post = relationship("Post", back_populates="animal")