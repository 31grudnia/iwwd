from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float, Boolean, Table, Text, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base
from database.models.OrderProductModel import OrderProduct


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), unique=True, nullable=False)
    short_description = Column(String(80), nullable=True)
    long_description = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    discount_amount = Column(Integer, nullable=True)

    rate = Column(Integer, nullable=True)
    ingredients = Column(String(256), nullable=True)
    dosage = Column(String(256), nullable=True)
    type = Column(String(10), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    subcategory_id = Column(Integer, ForeignKey("subcategory.id"), nullable=False)
    subcategory = relationship("Subcategory", back_populates="product")
    brand_id = Column(Integer, ForeignKey("brand.id"), nullable=False)
    brand = relationship("Brand", back_populates="product")

    order = relationship("Order", secondary=OrderProduct.__tablename__, back_populates="product")
    product_image = relationship("ProductImage", back_populates="product")

