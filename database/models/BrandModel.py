from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    photo = Column(String(80), nullable=False)
    description = Column(String(256), nullable=False)
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="brand")