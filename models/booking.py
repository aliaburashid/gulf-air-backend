from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from .base import BaseModel
from sqlalchemy.orm import relationship

class BookingModel(BaseModel):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True)  # Each booking reference must be unique
    user_id = Column(Integer, ForeignKey('users.id'))
    flight_id = Column(Integer, ForeignKey('flights.id'))
    passenger_name = Column(String)
    passenger_email = Column(String)
    seat_number = Column(String)
    booking_status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    total_price = Column(Float)
    booking_date = Column(DateTime)

    # Relationships
    # user = relationship('UserModel', back_populates='bookings')
    # flight = relationship('FlightModel', back_populates='bookings')
