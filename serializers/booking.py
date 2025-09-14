from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import UserResponseSchema
from .flight import FlightSchema

class BookingSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    booking_reference: str
    user_id: int
    flight_id: int
    passenger_name: str
    passenger_email: str
    seat_number: str
    booking_status: str = "confirmed"
    total_price: float
    booking_date: datetime
    user: Optional[UserResponseSchema] = None
    flight: Optional[FlightSchema] = None

    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    flight_id: int
    passenger_name: str
    passenger_email: str
    seat_number: str
    total_price: float

class BookingUpdate(BaseModel):
    passenger_name: Optional[str] = None
    passenger_email: Optional[str] = None
    seat_number: Optional[str] = None
    booking_status: Optional[str] = None
    total_price: Optional[float] = None
