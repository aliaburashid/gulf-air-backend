from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship

class FlightModel(BaseModel):

    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True)  # Each flight number must be unique
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    aircraft_type = Column(String)
    price = Column(Float)
    available_seats = Column(Integer)
    total_seats = Column(Integer)
    status = Column(String, default="scheduled")  # scheduled, delayed, cancelled, completed

    # Relationships - a flight can have multiple bookings
    # bookings = relationship('BookingModel', back_populates='flight')
