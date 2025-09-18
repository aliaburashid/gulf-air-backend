# =============================================================================
# FLIGHT MODEL - Stores individual flight information
# =============================================================================
# This model stores details about each specific flight (route, time, pricing, availability)
# Each flight is linked to an aircraft and has separate pricing for economy/business classes

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship

class FlightModel(BaseModel):
    """Flight model - stores information about individual flights"""

    __tablename__ = "flights"  # Database table name

    # Basic flight identification
    id = Column(Integer, primary_key=True, index=True)  # Unique flight ID
    flight_number = Column(String, unique=True)  # Flight number like "GF001", "GF002"
    
    # Route information - where the flight goes
    departure_airport = Column(String)  # Airport code like "BAH" (Bahrain)
    arrival_airport = Column(String)    # Airport code like "DXB" (Dubai)
    
    # Schedule information - when the flight operates
    departure_time = Column(DateTime)  # When the flight leaves
    arrival_time = Column(DateTime)    # When the flight arrives
    
    # Aircraft information - which plane is used
    aircraft_id = Column(Integer, ForeignKey('aircraft.id'))  # Links to aircraft table
    
    # Pricing - different prices for different seat classes
    economy_price = Column(Float)   # Price for economy class seats
    business_price = Column(Float)  # Price for business class seats (usually 2.5x economy)
    
    # Seat availability - how many seats are still available
    available_economy_seats = Column(Integer)   # Available economy seats
    available_business_seats = Column(Integer)  # Available business seats
    
    # Flight status - current state of the flight
    status = Column(String, default="scheduled")  # Options: scheduled, delayed, cancelled, completed
    
    # Relationship to aircraft
    aircraft = relationship('AircraftModel')

    # Relationship to bookings (a flight can have many bookings)
    bookings = relationship('BookingModel', back_populates='flight', lazy='dynamic')
