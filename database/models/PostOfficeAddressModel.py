from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PostOfficeAddress(Base):
    __tablename__ = "post_office_address"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(80), nullable=False)
    street = Column(String(80), nullable=False)
    building_number = Column(String(10), nullable=False)
    longtitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    post_office = relationship("PostOffice", uselist=False, back_populates="post_office_address")

