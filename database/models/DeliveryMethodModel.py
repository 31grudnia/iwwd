from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class DeliveryMethod(Base):
    __tablename__ = "delivery_method"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    logo = Column(String(255), nullable=False)
    delivery_payment = Column(Float, nullable=False)
    delivery_time = Column(DateTime(timezone=True), nullable=False)
    postal_points = Column(ARRAY(Integer), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    order_id = Column(Integer, ForeignKey("order.id"), nullable=True)
    order = relationship("Order", back_populates="delivery_method")