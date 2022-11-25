from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PostOffice(Base):
    __tablename__ = "post_office"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    address = Column(String(100), nullable=False)
    longtitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    delivery_time = Column(Date, nullable=False)
    delivery_price = Column(Float, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", back_populates="post_office")

    post_office_open_time = relationship("PostOfficeOpenTime", back_populates="post_office")