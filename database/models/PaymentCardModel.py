from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class PaymentCard(Base):
    __tablename__ = "payment_card"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(16), unique=True, nullable=False)
    expiration_date = Column(Date, nullable=False)
    cvc = Column(String(3), nullable=False)
    owner_name = Column(String(50), nullable=False)
    owner_surname = Column(String(50), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="payment_card")
