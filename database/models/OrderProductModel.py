from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func

from database.db_setup import Base


class OrderProduct(Base):
    __tablename__ = "order_product"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(ForeignKey("order.id"), primary_key=True)
    product_id = Column(ForeignKey("product.id"), primary_key=True)
    amount = Column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())