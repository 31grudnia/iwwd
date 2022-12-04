from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(30), nullable=True)
    state = Column(String(30), nullable=True)
    street = Column(String(40), nullable=True)
    home_number = Column(String(10), nullable=True)
    post_code = Column(String(6), nullable=True)
    user_id = Column(Integer, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="address")
