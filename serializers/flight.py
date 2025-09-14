from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

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
        orm_mode = True

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
    status: str = "scheduled"

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
