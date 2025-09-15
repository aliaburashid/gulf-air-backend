# =============================================================================
# BOOKINGS CONTROLLER - Handles all booking-related API endpoints
# This controller manages flight bookings including creation, updates, cancellations
# and check-in functionality. It includes complex business logic for seat management.
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.booking import BookingModel
from models.flight import FlightModel
from serializers.booking import BookingSchema, BookingCreate as BookingCreateSchema, BookingUpdate as BookingUpdateSchema
from models.user import UserModel
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user
import uuid
from datetime import datetime

router = APIRouter()


# =============================================================================
# GET USER'S BOOKINGS - Returns all bookings for the logged-in user
# This endpoint shows all bookings made by the current user
# Only shows bookings that belong to the authenticated user
# =============================================================================

@router.get('/bookings', response_model=List[BookingSchema])
def get_bookings(db: Session=Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Get all bookings for the current user"""
    bookings = db.query(BookingModel).filter(BookingModel.user_id == current_user.id).all()
    return bookings

# =============================================================================
# GET SINGLE BOOKING - Returns one specific booking by ID
# This endpoint shows details of a specific booking
# Only works if the booking belongs to the current user
# =============================================================================

@router.get("/bookings/{booking_id}", response_model=BookingSchema)
def get_single_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Get a specific booking by ID (only if it belongs to the current user)"""
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# =============================================================================
# CREATE NEW BOOKING - Creates a new flight booking with validation
# This is the most complex endpoint - it handles seat availability, validation,
# and updates flight seat counts. Includes business logic for seat management.
# =============================================================================

@router.post("/bookings", response_model=BookingSchema)
def create_booking(booking: BookingCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Create a new flight booking with seat validation and availability checks"""
    
    # STEP 1: Validate that the flight exists
    flight = db.query(FlightModel).filter(FlightModel.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # STEP 2: Check seat availability by class (economy vs falcon_gold)
    if booking.seat_class == "economy":
        if flight.available_economy_seats <= 0:
            raise HTTPException(status_code=400, detail="No available economy seats on this flight")
    elif booking.seat_class == "falcon_gold":
        if flight.available_falcon_gold_seats <= 0:
            raise HTTPException(status_code=400, detail="No available Falcon Gold seats on this flight")
    else:
        raise HTTPException(status_code=400, detail="Invalid seat class. Must be 'economy' or 'falcon_gold'")
    
    # STEP 3: Check if the specific seat is already taken
    existing_booking = db.query(BookingModel).filter(
        BookingModel.flight_id == booking.flight_id,
        BookingModel.seat_number == booking.seat_number,
        BookingModel.booking_status == "confirmed"
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Seat already taken")
    
    # STEP 4: Generate unique booking reference (Gulf Air format)
    booking_reference = f"GA{str(uuid.uuid4())[:8].upper()}"
    
    # STEP 5: Create the booking record
    new_booking = BookingModel(
        booking_reference=booking_reference,
        user_id=current_user.id,
        flight_id=booking.flight_id,
        passenger_name=booking.passenger_name,
        passenger_email=booking.passenger_email,
        passport_number=booking.passport_number,
        seat_class=booking.seat_class,
        seat_number=booking.seat_number,
        total_price=booking.total_price,
        booking_date=datetime.now()
    )
    
    db.add(new_booking)
    
    # STEP 6: Update flight seat availability (reduce available seats)
    if booking.seat_class == "economy":
        flight.available_economy_seats -= 1
    elif booking.seat_class == "falcon_gold":
        flight.available_falcon_gold_seats -= 1
    
    # STEP 7: Save everything to database
    db.commit()
    db.refresh(new_booking)
    return new_booking

# =============================================================================
# UPDATE BOOKING - Allows users to modify their booking details
# Users can update passenger information, seat selection, etc.
# Only works for bookings that belong to the current user
# =============================================================================
@router.put("/bookings/{booking_id}", response_model=BookingSchema)
def update_booking(booking_id: int, booking: BookingUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Update booking details (only if it belongs to the current user)"""
    
    # Find the booking and verify ownership
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Update only the fields that were provided (partial updates)
    booking_data = booking.dict(exclude_unset=True, exclude={'id'})
    for key, value in booking_data.items():
        setattr(db_booking, key, value)

    db.commit()  # Save changes to database
    db.refresh(db_booking)  # Get updated data
    return db_booking


# =============================================================================
# CANCEL BOOKING - Cancels a booking and returns seats to availability
# When a booking is cancelled, the seat becomes available again
# Updates both booking status and flight seat availability
# =============================================================================

@router.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Cancel a booking and return the seat to available seats"""
    
    # Find the booking and verify ownership
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check if already cancelled
    if db_booking.booking_status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    # Mark booking as cancelled
    db_booking.booking_status = "cancelled"
    
    # Return the seat to available seats on the flight
    flight = db.query(FlightModel).filter(FlightModel.id == db_booking.flight_id).first()
    if flight:
        if db_booking.seat_class == "economy":
            flight.available_economy_seats += 1
        elif db_booking.seat_class == "falcon_gold":
            flight.available_falcon_gold_seats += 1

    db.commit()  # Save changes
    return {"message": f"Booking {db_booking.booking_reference} has been cancelled"}

# =============================================================================
# FIND BOOKING BY REFERENCE - Find booking using booking reference number
# This is useful for passengers who only have their booking reference
# No authentication required - anyone with the reference can view the booking
# =============================================================================

@router.get("/bookings/reference/{booking_reference}", response_model=BookingSchema)
def get_booking_by_reference(booking_reference: str, db: Session = Depends(get_db)):
    """Find a booking using its reference number (like GA8C30A70F)"""
    booking = db.query(BookingModel).filter(BookingModel.booking_reference == booking_reference).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# =============================================================================
# CHECK-IN BOOKING - Allows passengers to check in for their flight
# This simulates the check-in process at the airport
# Only confirmed bookings can be checked in, and only 24 hours before departure
# =============================================================================

@router.post("/bookings/{booking_id}/checkin")
def check_in_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Check in for a flight booking - available 24 hours before departure"""
    
    # Find the booking and verify ownership
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only confirmed bookings can be checked in
    if db_booking.booking_status != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed bookings can be checked in")
    
    # Get the flight information to check departure time
    flight = db.query(FlightModel).filter(FlightModel.id == db_booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Check if check-in is available (24 hours before departure)
    from datetime import datetime, timedelta
    current_time = datetime.now()
    check_in_opens = flight.departure_time - timedelta(hours=24)
    
    if current_time < check_in_opens:
        hours_until_checkin = (check_in_opens - current_time).total_seconds() / 3600
        raise HTTPException(
            status_code=400, 
            detail=f"Check-in opens 24 hours before departure. Check-in available in {hours_until_checkin:.1f} hours"
        )
    
    # Check if check-in is still open (usually closes 1 hour before departure)
    check_in_closes = flight.departure_time - timedelta(hours=1)
    if current_time > check_in_closes:
        raise HTTPException(
            status_code=400, 
            detail="Check-in has closed. Please check in at the airport"
        )
    
    # Mark booking as checked in
    db_booking.booking_status = "checked_in"
    db.commit()
    
    return {
        "message": f"Successfully checked in for booking {db_booking.booking_reference}",
        "flight_number": flight.flight_number,
        "departure_time": flight.departure_time,
        "seat_number": db_booking.seat_number,
        "seat_class": db_booking.seat_class
    }
