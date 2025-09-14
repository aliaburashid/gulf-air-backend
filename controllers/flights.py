from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.flight import FlightModel
from serializers.flight import FlightSchema, FlightCreate as FlightCreateSchema, FlightUpdate as FlightUpdateSchema
from typing import List
from database import get_db

router = APIRouter()


# ------------------------
# Get all flights
# ------------------------
@router.get('/flights', response_model=List[FlightSchema])
def get_flights(db: Session=Depends(get_db)):
    flights = db.query(FlightModel).all()
    return flights


# ------------------------
# Get on flight by ID
# ------------------------
@router.get("/flights/{flight_id}", response_model=FlightSchema)
def get_single_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(FlightModel).filter(FlightModel.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


# ------------------------
# Create a new flight (with validation)
# ------------------------
@router.post("/flights", response_model=FlightSchema)
def create_flight(flight: FlightCreateSchema, db: Session = Depends(get_db)):
    # Check if flight number already exists
    existing_flight = db.query(FlightModel).filter(FlightModel.flight_number == flight.flight_number).first()
    if existing_flight:
        raise HTTPException(status_code=400, detail="Flight number already exists")
    
    
    new_flight = FlightModel(**flight.dict())  # Unpack all data into the model
    
    # save in the database
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)  # Refresh to get the new ID
    return new_flight


# ------------------------
# Update an existing flight
# ------------------------
@router.put("/flights/{flight_id}", response_model=FlightSchema)
def update_flight(flight_id: int, flight: FlightUpdateSchema, db: Session = Depends(get_db)):
    db_flight = db.query(FlightModel).filter(FlightModel.id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # only upate the fields provided 
    flight_data = flight.dict(exclude_unset=True, exclude={'id'}) 
    for key, value in flight_data.items():
        setattr(db_flight, key, value)

    db.commit()  # Save changes
    db.refresh(db_flight)  # Refresh to get updated data
    return db_flight



# ------------------------
# Delete a flight
# ------------------------
@router.delete("/flights/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = db.query(FlightModel).filter(FlightModel.id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(db_flight)  # Remove from database
    db.commit()  # Save changes
    return {"message": f"Flight with ID {flight_id} has been deleted"}



# ------------------------
# Search flight by departure and arrival 
# ------------------------
@router.get("/flights/search/{departure_airport}/{arrival_airport}")
def search_flights(departure_airport: str, arrival_airport: str, db: Session = Depends(get_db)):
    flights = db.query(FlightModel).filter(
        FlightModel.departure_airport == departure_airport,
        FlightModel.arrival_airport == arrival_airport,
        #  only upcoming scheduled flights 
        FlightModel.status == "scheduled"
    ).all()
    return flights


# ------------------------
# Get the status of a flight by flight number
# ------------------------
@router.get("/flights/status/{flight_number}")
def get_flight_status(flight_number: str, db: Session = Depends(get_db)):
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
