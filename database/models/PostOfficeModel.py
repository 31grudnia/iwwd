from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PostOffice(Base):
    __tablename__ = "post_office"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", back_populates="post_office")
    post_office_address_id = Column(Integer, ForeignKey('post_office_address.id'), nullable=False)
    post_office_address = relationship("PostOfficeAddress", back_populates="post_office")

    post_office_work_time = relationship("PostOfficeWorkTime", back_populates="post_office")