from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base

class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    birth_date = Column(Date, nullable=True)
    sex = Column(String(6))
    weight = Column(Float)
    height = Column(Float)
    photo = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    pins = Column(Integer, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")