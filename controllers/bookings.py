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

@router.get('/bookings', response_model=List[BookingSchema])
def get_bookings(db: Session=Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    bookings = db.query(BookingModel).filter(BookingModel.user_id == current_user.id).all()
    return bookings

@router.get("/bookings/{booking_id}", response_model=BookingSchema)
def get_single_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/bookings", response_model=BookingSchema)
def create_booking(booking: BookingCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # Check if flight exists
    flight = db.query(FlightModel).filter(FlightModel.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Check if flight has available seats
    if flight.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No available seats on this flight")
    
    # Check if seat is already taken
    existing_booking = db.query(BookingModel).filter(
        BookingModel.flight_id == booking.flight_id,
        BookingModel.seat_number == booking.seat_number,
        BookingModel.booking_status == "confirmed"
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Seat already taken")
    
    # Generate unique booking reference
    booking_reference = f"GA{str(uuid.uuid4())[:8].upper()}"
    
    new_booking = BookingModel(
        booking_reference=booking_reference,
        user_id=current_user.id,
        flight_id=booking.flight_id,
        passenger_name=booking.passenger_name,
        passenger_email=booking.passenger_email,
        seat_number=booking.seat_number,
        total_price=booking.total_price,
        booking_date=datetime.now()
    )
    
    db.add(new_booking)
    
    # Update available seats
    flight.available_seats -= 1
    
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.put("/bookings/{booking_id}", response_model=BookingSchema)
def update_booking(booking_id: int, booking: BookingUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking_data = booking.dict(exclude_unset=True, exclude={'id'})  # Only update the fields provided
    for key, value in booking_data.items():
        setattr(db_booking, key, value)

    db.commit()  # Save changes
    db.refresh(db_booking)  # Refresh to get updated data
    return db_booking

@router.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if db_booking.booking_status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    # Update booking status to cancelled
    db_booking.booking_status = "cancelled"
    
    # Return seat to available seats
    flight = db.query(FlightModel).filter(FlightModel.id == db_booking.flight_id).first()
    if flight:
        flight.available_seats += 1

    db.commit()  # Save changes
    return {"message": f"Booking {db_booking.booking_reference} has been cancelled"}

@router.get("/bookings/reference/{booking_reference}", response_model=BookingSchema)
def get_booking_by_reference(booking_reference: str, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.booking_reference == booking_reference).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/bookings/{booking_id}/checkin")
def check_in_booking(booking_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if db_booking.booking_status != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed bookings can be checked in")
    
    # Update booking status to checked in
    db_booking.booking_status = "checked_in"
    db.commit()
    
    return {"message": f"Successfully checked in for booking {db_booking.booking_reference}"}
