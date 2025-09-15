# =============================================================================
# BOOKING MODEL - Stores passenger flight bookings
# This model links users to flights and stores all booking details
# Includes passenger information, seat selection, and payment details
# =============================================================================

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from .base import BaseModel
from sqlalchemy.orm import relationship

class BookingModel(BaseModel):
    """Booking model - stores passenger flight bookings"""

    __tablename__ = "bookings"  # Database table name

    # Basic booking identification
    id = Column(Integer, primary_key=True, index=True)  # Unique booking ID
    booking_reference = Column(String, unique=True)  # Unique code like "GA8C30A70F"
    
    # Links to other tables - who booked what flight
    user_id = Column(Integer, ForeignKey('users.id'))    # Which user made the booking
    flight_id = Column(Integer, ForeignKey('flights.id')) # Which flight was booked
    
    # Passenger information - who is traveling
    passenger_name = Column(String)     # Full name of the passenger
    passenger_email = Column(String)    # Email address for notifications
    passport_number = Column(String)    # Required for international flights
    
    # Seat information - where the passenger sits
    seat_class = Column(String, default="economy")  # "economy" or "falcon_gold"
    seat_number = Column(String)  # Specific seat like "12A", "1B"
    
    # Booking status and payment
    booking_status = Column(String, default="confirmed")  # confirmed, cancelled, checked_in
    total_price = Column(Float)  # Amount paid for the booking
    booking_date = Column(DateTime)  # When the booking was made

    # Relationship to other tables: Each booking connects a user to a flight.
    user = relationship('UserModel', back_populates='bookings')
    flight = relationship('FlightModel', back_populates='bookings')
