from sqlalchemy import Column, DateTime, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database.db_setup import Base

class UserSex(enum.Enum):
    male = 1
    female = 2

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    city = Column(String(30), nullable=True)
    email = Column(String(50), unique=True)
    age = Column(Integer)
    phone_number = Column(String(15), unique=True)
    login = Column(String(50), unique=True)
    password = Column(String(80))
    photo = Column(String(50), nullable=True)
    regulations = Column(Integer, nullable=True)
    sex = Column(Enum(UserSex))
    hidden_posts = Column(Integer, nullable=True)
    coins = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal = relationship("Animal", back_populates="user")
    post = relationship("Post", back_populates="user")
    walk = relationship("Walk", back_populates="user")