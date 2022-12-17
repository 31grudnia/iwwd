from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PaymentMethodCategory(Base):
    __tablename__ = "payment_method_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    payment_method = relationship("PaymentMethod", back_populates="payment_method_category")


