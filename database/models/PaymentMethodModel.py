from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    photo = Column(String(80), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship("Order", back_populates="payment_method")

    payment_method_category_id = Column(Integer, ForeignKey("payment_method_category.id"), nullable=False)
    payment_method_category = relationship("PaymentMethodCategory", back_populates="payment_method")