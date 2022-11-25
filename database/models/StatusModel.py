from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship("Order", back_populates="status")
