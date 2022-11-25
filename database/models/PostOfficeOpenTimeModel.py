from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PostOfficeOpenTime(Base):
    __tablename__ = "post_office_open_time"

    id = Column(Integer, primary_key=True, index=True)
    open_time = Column(DateTime(timezone=True))
    close_time = Column(DateTime(timezone=True))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    post_office_id = Column(Integer, ForeignKey("post_office.id"), nullable=False)
    post_office = relationship("PostOffice", back_populates="post_office_open_time")