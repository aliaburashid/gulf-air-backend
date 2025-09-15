# =============================================================================
# FLIGHT SERIALIZERS - Data validation for flight operations
# These classes define how flight data is validated when sent to/from the API
# They ensure data is correct before saving to database and format responses properly
# =============================================================================

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# =============================================================================
# FLIGHT SCHEMA - For reading/displaying flight data
# Used when returning flight information to the frontend
# Includes all flight details that users need to see
# =============================================================================

class FlightSchema(BaseModel):
    id: Optional[int] = Field(default=None)  # Flight ID (auto-generated)
    flight_number: str  # Flight number like "GF001"
    departure_airport: str  # Airport code like "BAH"
    arrival_airport: str    # Airport code like "DXB"
    departure_time: datetime  # When flight leaves
    arrival_time: datetime    # When flight arrives
    aircraft_id: int  # Which aircraft is used
    economy_price: float   # Economy class price
    falcon_gold_price: float  # Falcon Gold class price
    available_economy_seats: int   # Available economy seats
    available_falcon_gold_seats: int  # Available Falcon Gold seats
    status: str = "scheduled"  # Flight status

    class Config:
        orm_mode = True  # Allows working with database objects directly

# =============================================================================
# FLIGHT CREATE - For creating new flights
# Used when admin creates a new flight
# All fields are required to create a complete flight record
# =============================================================================

class FlightCreate(BaseModel):
    flight_number: str  # Must be unique
    departure_airport: str  # Airport code
    arrival_airport: str    # Airport code
    departure_time: datetime  # Scheduled departure
    arrival_time: datetime    # Scheduled arrival
    aircraft_id: int  # Which aircraft to use
    economy_price: float   # Economy class price
    falcon_gold_price: float  # Falcon Gold class price
    available_economy_seats: int   # Starting economy seats
    available_falcon_gold_seats: int  # Starting Falcon Gold seats
    status: str = "scheduled"  # Default status

# =============================================================================
# FLIGHT UPDATE - For updating existing flights
# Used when admin updates flight information
# All fields are optional - only update what's provided
# =============================================================================

class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    aircraft_id: Optional[int] = None
    economy_price: Optional[float] = None
    falcon_gold_price: Optional[float] = None
    available_economy_seats: Optional[int] = None
    available_falcon_gold_seats: Optional[int] = None
    status: Optional[str] = None
