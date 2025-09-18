# =============================================================================
# BOOKINGS CONTROLLER - Handles all booking-related API endpoints
# =============================================================================
# This controller manages flight bookings including creation, updates, cancellations
# and check-in functionality. It includes complex business logic for seat management.

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.booking import BookingModel
from models.flight import FlightModel
from serializers.booking import BookingSchema, BookingCreate as BookingCreateSchema, BookingUpdate as BookingUpdateSchema
from pydantic import BaseModel
from models.user import UserModel
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user
import random
import string
import uuid
from datetime import datetime
import random
import string
import math

router = APIRouter()


# =============================================================================
# LOYALTY PROGRAM UTILITIES - Calculate miles and points for flights
# =============================================================================

def calculate_flight_distance(departure_airport: str, arrival_airport: str) -> int:
    """Calculate approximate flight distance in miles between two airports"""
    # Simple airport coordinates for major Gulf Air destinations
    airport_coords = {
        "BAH": (26.2708, 50.6336),  # Bahrain
        "DXB": (25.2532, 55.3657),  # Dubai
        "DOH": (25.2611, 51.5651),  # Doha
        "KWI": (29.2269, 47.9789),  # Kuwait
        "RUH": (24.6408, 46.7728),  # Riyadh
        "JED": (21.6796, 39.1565),  # Jeddah
        "CAI": (30.1127, 31.4000),  # Cairo
        "BEY": (33.8209, 35.4883),  # Beirut
        "AMM": (31.7225, 35.9933),  # Amman
        "LHR": (51.4700, -0.4543),  # London
        "CDG": (49.0097, 2.5479),   # Paris
        "FRA": (50.0379, 8.5622),   # Frankfurt
        "MAD": (40.4839, -3.5680),  # Madrid
        "FCO": (41.8003, 12.2389),  # Rome
        "ATH": (37.9364, 23.9445),  # Athens
        "BOM": (19.0896, 72.8656),  # Mumbai
        "DEL": (28.5562, 77.1000),  # Delhi
        "BKK": (13.6900, 100.7501), # Bangkok
        "KUL": (2.7456, 101.7099),  # Kuala Lumpur
        "SIN": (1.3644, 103.9915),  # Singapore
        "HKG": (22.3080, 113.9185), # Hong Kong
        "NBO": (-1.3192, 36.9278),  # Nairobi
        "JNB": (-26.1367, 28.2411), # Johannesburg
    }
    
    if departure_airport not in airport_coords or arrival_airport not in airport_coords:
        # Default distance for unknown airports
        return 500
    
    # Get coordinates
    lat1, lon1 = airport_coords[departure_airport]
    lat2, lon2 = airport_coords[arrival_airport]
    
    # Haversine formula to calculate distance
    R = 3959  # Earth's radius in miles
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return int(distance)


def calculate_miles_earned(distance: int, seat_class: str, loyalty_tier: str) -> int:
    """Calculate miles earned based on distance, seat class, and loyalty tier"""
    # Base miles = distance
    base_miles = distance
    
    # Seat class multiplier
    if seat_class == "business":
        seat_multiplier = 1.5  # Business class gets 50% bonus
    else:
        seat_multiplier = 1.0  # Economy class gets base miles
    
    # Loyalty tier multiplier
    tier_multipliers = {
        "BLUE": 1.0,      # Base tier
        "SILVER": 1.25,   # 25% bonus
        "GOLD": 1.5,      # 50% bonus
        "PLATINUM": 2.0   # 100% bonus
    }
    
    tier_multiplier = tier_multipliers.get(loyalty_tier, 1.0)
    
    # Calculate total miles
    total_miles = int(base_miles * seat_multiplier * tier_multiplier)
    
    return total_miles


def calculate_points_earned(miles: int) -> int:
    """Calculate loyalty points earned (typically 1 point per 10 miles)"""
    return miles // 10


def check_and_upgrade_loyalty_tier(user: UserModel) -> dict:
    """Check if user qualifies for tier upgrade based on total loyalty points"""
    total_points = user.loyalty_points or 0
    current_tier = user.loyalty_tier or "BLUE"
    
    # Define tier thresholds (loyalty points required for each tier)
    tier_thresholds = {
        "BLUE": 0,      # Starting tier
        "SILVER": 500,  # 500 points for Silver
        "GOLD": 1000,   # 1,000 points for Gold
        "PLATINUM": 2000 # 2,000 points for Platinum
    }
    
    # Determine what tier the user should be based on points
    new_tier = "BLUE"
    for tier, threshold in sorted(tier_thresholds.items(), key=lambda x: x[1], reverse=True):
        if total_points >= threshold:
            new_tier = tier
            break
    
    # Check if user was upgraded
    tier_upgraded = False
    if new_tier != current_tier:
        tier_upgraded = True
        user.loyalty_tier = new_tier
    
    return {
        "tier_upgraded": tier_upgraded,
        "old_tier": current_tier,
        "new_tier": new_tier,
        "total_points": total_points,
        "next_tier_threshold": get_next_tier_threshold(new_tier, tier_thresholds)
    }


def get_next_tier_threshold(current_tier: str, tier_thresholds: dict) -> int:
    """Get the miles threshold for the next tier up"""
    tier_order = ["BLUE", "SILVER", "GOLD", "PLATINUM"]
    current_index = tier_order.index(current_tier)
    
    if current_index < len(tier_order) - 1:
        next_tier = tier_order[current_index + 1]
        return tier_thresholds[next_tier]
    else:
        return None  # Already at highest tier


# =============================================================================
# GET USER'S BOOKINGS - Returns all bookings for the logged-in user
# =============================================================================
# This endpoint shows all bookings made by the current user
# Only shows bookings that belong to the authenticated user

@router.get('/bookings', response_model=List[BookingSchema])
def get_bookings(db: Session=Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Get all bookings for the current user"""
    bookings = db.query(BookingModel).filter(BookingModel.user_id == current_user.id).all()
    return bookings

# =============================================================================
# GET SINGLE BOOKING - Returns one specific booking by ID
# =============================================================================
# This endpoint shows details of a specific booking
# Only works if the booking belongs to the current user

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
# =============================================================================
# This is the most complex endpoint - it handles seat availability, validation,
# and updates flight seat counts. Includes business logic for seat management.

@router.post("/bookings", response_model=BookingSchema)
def create_booking(booking: BookingCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Create a new flight booking with seat validation and availability checks"""
    
    # STEP 1: Validate that the flight exists
    flight = db.query(FlightModel).filter(FlightModel.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # STEP 2: Check seat availability by class (economy vs business)
    if booking.seat_class == "economy":
        if flight.available_economy_seats <= 0:
            raise HTTPException(status_code=400, detail="No available economy seats on this flight")
    elif booking.seat_class == "business":
        if flight.available_business_seats <= 0:
            raise HTTPException(status_code=400, detail="No available business seats on this flight")
    else:
        raise HTTPException(status_code=400, detail="Invalid seat class. Must be 'economy' or 'business'")
    
    # STEP 3: Check if the specific seat is already taken
    existing_booking = db.query(BookingModel).filter(
        BookingModel.flight_id == booking.flight_id,
        BookingModel.seat_number == booking.seat_number,
        BookingModel.booking_status == "confirmed"
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Seat already taken")
    
    # STEP 4: Generate unique booking reference (6 random letters)
    booking_reference = ''.join(random.choices(string.ascii_uppercase, k=6))
    
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
    elif booking.seat_class == "business":
        flight.available_business_seats -= 1
    
    # STEP 7: Save everything to database
    db.commit()
    db.refresh(new_booking)
    return new_booking

# =============================================================================
# UPDATE BOOKING - Allows users to modify their booking details
# =============================================================================
# Users can update passenger information, seat selection, etc.
# Only works for bookings that belong to the current user

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
# =============================================================================
# When a booking is cancelled, the seat becomes available again
# Updates both booking status and flight seat availability

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
        elif db_booking.seat_class == "business":
            flight.available_business_seats += 1

    db.commit()  # Save changes
    return {
        "message": f"Booking {db_booking.booking_reference} has been cancelled",
        "booking_reference": db_booking.booking_reference,
        "refund_amount": db_booking.total_price,
        "status": "cancelled"
    }

# =============================================================================
# FIND BOOKING BY REFERENCE - Find booking using booking reference number
# =============================================================================
# This is useful for passengers who only have their booking reference
# No authentication required - anyone with the reference can view the booking

@router.get("/bookings/reference/{booking_reference}", response_model=BookingSchema)
def get_booking_by_reference(booking_reference: str, db: Session = Depends(get_db)):
    """Find a booking using its reference number (like GA8C30A70F)"""
    booking = db.query(BookingModel).filter(BookingModel.booking_reference == booking_reference).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# =============================================================================
# RESCHEDULE BOOKING - Allows passengers to change their flight
# =============================================================================
# This endpoint handles rescheduling by cancelling the old booking and creating a new one
# It maintains the same passenger information but changes the flight

class RescheduleRequest(BaseModel):
    new_flight_id: int
    seat_class: str | None = None  # optional class change
    seat_number: str | None = None  # optional seat change


@router.post("/bookings/{booking_id}/reschedule")
def reschedule_booking(booking_id: int, payload: RescheduleRequest, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Reschedule a booking to a different flight"""
    
    # Find the original booking and verify ownership
    original_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not original_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check if booking can be rescheduled
    if original_booking.booking_status == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot reschedule a cancelled booking")
    if original_booking.booking_status == "checked_in":
        raise HTTPException(status_code=400, detail="Cannot reschedule a checked-in booking")
    
    # Validate the new flight exists
    new_flight = db.query(FlightModel).filter(FlightModel.id == payload.new_flight_id).first()
    if not new_flight:
        raise HTTPException(status_code=404, detail="New flight not found")
    
    # Check seat availability on the new flight
    requested_seat_class = payload.seat_class or original_booking.seat_class
    requested_seat_number = payload.seat_number or original_booking.seat_number

    if requested_seat_class == "economy":
        if new_flight.available_economy_seats <= 0:
            raise HTTPException(status_code=400, detail="No available economy seats on the new flight")
    elif requested_seat_class == "business":
        if new_flight.available_business_seats <= 0:
            raise HTTPException(status_code=400, detail="No available business seats on the new flight")
    
    # Check if the same seat is available on the new flight
    existing_booking = db.query(BookingModel).filter(
        BookingModel.flight_id == payload.new_flight_id,
        BookingModel.seat_number == requested_seat_number,
        BookingModel.booking_status == "confirmed"
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Your preferred seat is not available on the new flight")
    
    # Cancel the original booking (return seat to availability)
    original_booking.booking_status = "cancelled"
    original_flight = db.query(FlightModel).filter(FlightModel.id == original_booking.flight_id).first()
    if original_flight:
        if original_booking.seat_class == "economy":
            original_flight.available_economy_seats += 1
        elif original_booking.seat_class == "business":
            original_flight.available_business_seats += 1
    
    # Create new unique booking reference (6 uppercase letters)
    new_reference = ''.join(random.choices(string.ascii_uppercase, k=6))
    while db.query(BookingModel).filter(BookingModel.booking_reference == new_reference).first():
        new_reference = ''.join(random.choices(string.ascii_uppercase, k=6))

    # Create new booking with same passenger info but new flight
    new_booking = BookingModel(
        booking_reference=new_reference,
        user_id=current_user.id,
        flight_id=payload.new_flight_id,
        passenger_name=original_booking.passenger_name,
        passenger_email=original_booking.passenger_email,
        passport_number=original_booking.passport_number,
        seat_class=requested_seat_class,
        seat_number=requested_seat_number,
        total_price=original_booking.total_price,  # Keep same price for now
        booking_date=datetime.now()
    )
    
    db.add(new_booking)
    
    # Update new flight seat availability
    if requested_seat_class == "economy":
        new_flight.available_economy_seats -= 1
    elif requested_seat_class == "business":
        new_flight.available_business_seats -= 1
    
    db.commit()
    db.refresh(new_booking)
    
    return {
        "message": f"Booking {original_booking.booking_reference} has been rescheduled successfully",
        "new_booking": new_booking
    }


# =============================================================================
# CHECK-IN BOOKING - Allows passengers to check in for their flight
# =============================================================================
# This simulates the check-in process at the airport
# Only confirmed bookings can be checked in

@router.post("/bookings/{booking_id}/checkin")
def check_in_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Check in for a flight booking and award loyalty miles/points"""
    
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
    
    # Get the flight details for miles calculation
    flight = db.query(FlightModel).filter(FlightModel.id == db_booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Calculate miles and points earned
    distance = calculate_flight_distance(flight.departure_airport, flight.arrival_airport)
    miles_earned = calculate_miles_earned(distance, db_booking.seat_class, current_user.loyalty_tier or "BLUE")
    points_earned = calculate_points_earned(miles_earned)
    
    # Update user's loyalty data
    current_user.loyalty_miles = (current_user.loyalty_miles or 0) + miles_earned
    current_user.loyalty_points = (current_user.loyalty_points or 0) + points_earned
    
    # Check for tier upgrade after adding miles
    tier_upgrade_info = check_and_upgrade_loyalty_tier(current_user)
    
    # Mark booking as checked in
    db_booking.booking_status = "checked_in"
    
    # Save all changes
    db.commit()
    db.refresh(current_user)
    
    # Prepare response with tier upgrade information
    response_data = {
        "message": f"Successfully checked in for booking {db_booking.booking_reference}",
        "loyalty_rewards": {
            "miles_earned": miles_earned,
            "points_earned": points_earned,
            "total_miles": current_user.loyalty_miles,
            "total_points": current_user.loyalty_points,
            "flight_distance": distance,
            "seat_class": db_booking.seat_class,
            "loyalty_tier": current_user.loyalty_tier
        }
    }
    
    # Add tier upgrade information if user was upgraded
    if tier_upgrade_info["tier_upgraded"]:
        response_data["tier_upgrade"] = {
            "upgraded": True,
            "old_tier": tier_upgrade_info["old_tier"],
            "new_tier": tier_upgrade_info["new_tier"],
            "total_points": tier_upgrade_info["total_points"],
            "next_tier_threshold": tier_upgrade_info["next_tier_threshold"]
        }
    else:
        response_data["tier_upgrade"] = {
            "upgraded": False,
            "current_tier": current_user.loyalty_tier,
            "total_points": current_user.loyalty_points,
            "next_tier_threshold": tier_upgrade_info["next_tier_threshold"]
        }
    
    return response_data

