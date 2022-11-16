from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    # photo = Column()
    text = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False)
    reports = Column(Integer, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="post")

