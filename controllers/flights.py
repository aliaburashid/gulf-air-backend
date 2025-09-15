# =============================================================================
# FLIGHTS CONTROLLER - User-facing flight endpoints only
# This controller provides read-only access to flight information for users
# Users can view flights, search flights, and check flight status
# Flight creation/updates are handled by data seeding, not user endpoints
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.flight import FlightModel
from serializers.flight import FlightSchema
from typing import List
from database import get_db

router = APIRouter()

# =============================================================================
# GET ALL FLIGHTS - View all available flights
# Users can browse all available flights in the system
# This is useful for general browsing and discovery
# =============================================================================

@router.get('/flights', response_model=List[FlightSchema])
def get_flights(db: Session=Depends(get_db)):
    """Get all available flights for users to browse"""
    flights = db.query(FlightModel).all()
    return flights

# =============================================================================
# GET SINGLE FLIGHT - View details of a specific flight
# Users can get detailed information about a specific flight
# Useful when they want to book a particular flight
# =============================================================================

@router.get("/flights/{flight_id}", response_model=FlightSchema)
def get_single_flight(flight_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific flight"""
    flight = db.query(FlightModel).filter(FlightModel.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

# =============================================================================
# SEARCH FLIGHTS - Find flights by route
# Users can search for flights between specific airports
# Only returns scheduled flights (not cancelled or completed)
# =============================================================================

@router.get("/flights/search/{departure_airport}/{arrival_airport}")
def search_flights(departure_airport: str, arrival_airport: str, db: Session = Depends(get_db)):
    """Search for flights between two airports"""
    flights = db.query(FlightModel).filter(
        FlightModel.departure_airport == departure_airport,
        FlightModel.arrival_airport == arrival_airport,
        FlightModel.status == "scheduled"  # Only upcoming scheduled flights
    ).all()
    return flights

# =============================================================================
# FLIGHT STATUS - Check the status of a specific flight
# Users can check if their flight is on time, delayed, or cancelled
# Useful for passengers to track their flight status
# =============================================================================
@router.get("/flights/status/{flight_number}")
def get_flight_status(flight_number: str, db: Session = Depends(get_db)):
    """Get the current status of a flight by flight number"""
    flight = db.query(FlightModel).filter(FlightModel.flight_number == flight_number).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return {
        "flight_number": flight.flight_number,
        "status": flight.status,
        "departure_airport": flight.departure_airport,
        "arrival_airport": flight.arrival_airport,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time
    }
