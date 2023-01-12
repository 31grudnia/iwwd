from sqlalchemy import Column, ForeignKey, Integer, Float, Time, ARRAY, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Walk(Base):
    __tablename__ = "walk"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time, nullable=False)
    distance = Column(Float, nullable=False)
    coins_gained = Column(Integer, nullable=False)
    photo_url = Column(String(255), nullable=False)

    animal_id = Column(ARRAY(Integer), ForeignKey("animal.id"), nullable=False)
    animal = relationship("Animal", back_populates="walk")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # ???
    user = relationship("User", back_populates="walk")


