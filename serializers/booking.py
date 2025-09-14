from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import UserResponseSchema
from .flight import FlightSchema

# Schema for reading/returning booking data
class BookingSchema(BaseModel):
    id: Optional[int] = Field(default=None) # Booking ID
    booking_reference: str  # Unique booking reference
    user_id: int # ID of the user who booked
    flight_id: int # ID of the booked flight
    passenger_name: str # Passenger name
    passenger_email: str # Passenger email
    seat_number: str # Assigned seat number
    booking_status: str = "confirmed" # Status: confirmed, cancelled, completed
    total_price: float # Total price of the booking
    booking_date: datetime # Date and time of booking
    user: Optional[UserResponseSchema] = None # Optional nested user info
    flight: Optional[FlightSchema] = None # Optional nested flight info

    class Config:
        orm_mode = True

# Schema for creating a new booking
class BookingCreate(BaseModel):
    flight_id: int
    passenger_name: str
    passenger_email: str
    seat_number: str
    total_price: float

# Schema for updating an existing booking
class BookingUpdate(BaseModel):
    passenger_name: Optional[str] = None
    passenger_email: Optional[str] = None
    seat_number: Optional[str] = None
    booking_status: Optional[str] = None
    total_price: Optional[float] = None
