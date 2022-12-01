from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base

from database.models.OrderProductModel import OrderProduct


class Order(Base):
    __tablename__ = "order"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String(15), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    status = relationship("Status", back_populates="order")
    payment_method_id = Column(Integer, ForeignKey("payment_method.id"), nullable=False)
    payment_method = relationship("PaymentMethod", back_populates="order")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="order")

    post_office = relationship("PostOffice", back_populates="order")
    product = relationship("Product", secondary=OrderProduct.__tablename__, back_populates="order")
