from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base

user_pin_table = Table(
    "user_pin_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("pin_id", ForeignKey("pin.id"), primary_key=True),
)


class Pin(Base):
    __tablename__ = "pin"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longtitude = Column(Float, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False)
    animal = relationship("Animal", back_populates="pin")

    user = relationship("User", secondary=user_pin_table, back_populates="pin")
