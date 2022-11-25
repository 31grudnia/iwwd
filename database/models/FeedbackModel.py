from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    rate = Column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("product", back_populates="feedback")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="feedback")
