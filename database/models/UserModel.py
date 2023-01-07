from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, LargeBinary, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db_setup import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    photo_url = Column(String(255), nullable=True)
    is_admin = Column(Boolean, nullable=False)
    coins = Column(Integer, nullable=False)
    favourites = Column(ARRAY(Integer), nullable=True)
    disabled = Column(Boolean, nullable=False)
    refresh_token = Column(String(255), nullable=True)
    recovery_token = Column(String(255), nullable=True)
    recovery_token_expiration = Column(DateTime(timezone=True))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    address = relationship("Address", back_populates="user")

    pin = relationship("Pin", back_populates="user")
    payment_card = relationship("PaymentCard", back_populates="user")
    order = relationship("Order", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")
    post = relationship("Post", back_populates="user")
    comment = relationship("Comment", back_populates="user")
    animal = relationship("Animal", back_populates="user")
    walk = relationship("Walk", back_populates="user")
