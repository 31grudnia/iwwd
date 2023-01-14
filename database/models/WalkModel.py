from sqlalchemy import Column, ForeignKey, Integer, Float, Time, ARRAY, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class Walk(Base):
    __tablename__ = "walk"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String(20), nullable=False)
    distance = Column(Float, nullable=False)
    coins_gained = Column(Integer, nullable=False)
    photo = Column(ARRAY(Integer), nullable=False)
    animals_id = Column(ARRAY(Integer), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="walk")


