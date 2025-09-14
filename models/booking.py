#  Links users to flights with booking details
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from .base import BaseModel
from sqlalchemy.orm import relationship

# Booking database model
class BookingModel(BaseModel):

    __tablename__ = "bookings"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True)  # Unique reference code for each booking
    user_id = Column(Integer, ForeignKey('users.id'))  # ID of the user who booked
    flight_id = Column(Integer, ForeignKey('flights.id')) # ID of the flight booked
    passenger_name = Column(String) # Name of the passenger
    passenger_email = Column(String)  # Email of the passenger
    seat_number = Column(String)  # Assigned seat number
    booking_status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    total_price = Column(Float)  # Total price paid for the booking
    booking_date = Column(DateTime) # Date and time of booking

    # Relationship to other tables: Each booking connects a user to a flight.
    user = relationship('UserModel', back_populates='bookings')
    flight = relationship('FlightModel', back_populates='bookings')
