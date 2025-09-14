# pydantic: a library used in FastAPI to validate and handle data easily.
# Validate input – Ensure incoming data is correct before saving to the database.
# Format output – Ensure data sent back to clients (API responses) has the right structure.
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# For reading/displaying flight data
class FlightSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    price: float
    available_seats: int
    total_seats: int
    status: str = "scheduled"

    class Config:
        # allows this Pydantic model to work directly with ORM/database objects
        orm_mode = True

# used when creating a new flight 
class FlightCreate(BaseModel):
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    price: float
    available_seats: int
    total_seats: int
    # Ensures the data sent by the user is valid before saving to the database.
    status: str = "scheduled"

# Used when updating an existing flight
# All fields are optional because the user might want to update only some fields, not all of them
class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    aircraft_type: Optional[str] = None
    price: Optional[float] = None
    available_seats: Optional[int] = None
    total_seats: Optional[int] = None
    status: Optional[str] = None
