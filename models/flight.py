# Defines flight information (routes, times, pricing, seats)

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship


# Flight database model
class FlightModel(BaseModel):

    __tablename__ = "flights"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True)  # Each flight number must be unique
    departure_airport = Column(String) # Departure airport code/name
    arrival_airport = Column(String) # Arrival airport code/name
    departure_time = Column(DateTime) # Scheduled departure date and time
    arrival_time = Column(DateTime) # Scheduled arrival date and time
    aircraft_type = Column(String) # Type/model of the plane
    price = Column(Float)  # Ticket price
    available_seats = Column(Integer) # Seats still available
    total_seats = Column(Integer) # Total number of seats on the plane
    status = Column(String, default="scheduled")  # scheduled, delayed, cancelled, completed

    # Relationship to bookings (a flight can have many bookings)
    bookings = relationship('BookingModel', back_populates='flight')
