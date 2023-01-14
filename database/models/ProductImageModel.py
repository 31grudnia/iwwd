from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(String(255), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="product_image")

