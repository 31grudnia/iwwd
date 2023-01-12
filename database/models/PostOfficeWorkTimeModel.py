from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PostOfficeWorkTime(Base):
    __tablename__ = "post_office_work_time"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    work_time = Column(String(30), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    post_office_id = Column(Integer, ForeignKey("post_office.id"), nullable=False)
    post_office = relationship("PostOffice", back_populates="post_office_work_time")