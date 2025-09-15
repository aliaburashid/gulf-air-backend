# =============================================================================
# BOOKING SERIALIZERS - Data validation for booking operations
# These classes define how booking data is validated when sent to/from the API
# They ensure passenger information is correct and handle seat class validation
# =============================================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user import UserResponseSchema
from .flight import FlightSchema

# =============================================================================
# BOOKING SCHEMA - For reading/returning booking data
# Used when returning booking information to the frontend
# Includes all booking details and optional nested user/flight information
# =============================================================================

class BookingSchema(BaseModel):
    id: Optional[int] = Field(default=None)  # Booking ID (auto-generated)
    booking_reference: str  # Unique reference like "GA8C30A70F"
    user_id: int  # Which user made the booking
    flight_id: int  # Which flight was booked
    passenger_name: str  # Full name of passenger
    passenger_email: str  # Email for notifications
    passport_number: str  # Required for international flights
    seat_class: str = "economy"  # "economy" or "falcon_gold"
    seat_number: str  # Specific seat like "12A"
    booking_status: str = "confirmed"  # confirmed, cancelled, checked_in
    total_price: float  # Amount paid
    booking_date: datetime  # When booking was made
    user: Optional[UserResponseSchema] = None  # Optional: include user details
    flight: Optional[FlightSchema] = None  # Optional: include flight details

    class Config:
        orm_mode = True  # Allows working with database objects directly

# =============================================================================
# BOOKING CREATE - For creating new bookings
# Used when a user makes a new flight booking
# All fields are required to create a complete booking
# =============================================================================
class BookingCreate(BaseModel):
    flight_id: int  # Which flight to book
    passenger_name: str  # Full name of passenger
    passenger_email: str  # Email for notifications
    passport_number: str  # Required for international flights
    seat_class: str = "economy"  # "economy" or "falcon_gold"
    seat_number: str  # Specific seat like "12A"
    total_price: float  # Amount to pay

# =============================================================================
# BOOKING UPDATE - For updating existing bookings
# Used when user wants to modify their booking
# All fields are optional - only update what's provided
# =============================================================================
class BookingUpdate(BaseModel):
    passenger_name: Optional[str] = None  # Change passenger name
    passenger_email: Optional[str] = None  # Change email
    passport_number: Optional[str] = None  # Update passport
    seat_class: Optional[str] = None  # Change seat class
    seat_number: Optional[str] = None  # Change seat number
    booking_status: Optional[str] = None  # Change status (admin only)
    total_price: Optional[float] = None  # Update price
