from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Subcategory(Base):
    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="subcategory")

    product = relationship("Product", back_populates="subcategory")
