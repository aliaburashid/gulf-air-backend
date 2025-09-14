# data/flight_data.py
from models.flight import FlightModel
from datetime import datetime, timedelta

def create_flights():
    # Create some sample flights for Gulf Air
    return [
    FlightModel(
        flight_number="GF001",
        departure_airport="BAH",
        arrival_airport="DXB",
        departure_time=datetime.now() + timedelta(days=1, hours=8),
        arrival_time=datetime.now() + timedelta(days=1, hours=10),
        aircraft_type="Boeing 737",
        price=299.99,
        available_seats=150,
        total_seats=180,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF002",
        departure_airport="DXB",
        arrival_airport="BAH",
        departure_time=datetime.now() + timedelta(days=2, hours=14),
        arrival_time=datetime.now() + timedelta(days=2, hours=16),
        aircraft_type="Airbus A320",
        price=279.99,
        available_seats=120,
        total_seats=150,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF003",
        departure_airport="BAH",
        arrival_airport="DOH",
        departure_time=datetime.now() + timedelta(days=3, hours=10),
        arrival_time=datetime.now() + timedelta(days=3, hours=11),
        aircraft_type="Boeing 737",
        price=199.99,
        available_seats=80,
        total_seats=100,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF004",
        departure_airport="DOH",
        arrival_airport="BAH",
        departure_time=datetime.now() + timedelta(days=4, hours=16),
        arrival_time=datetime.now() + timedelta(days=4, hours=17),
        aircraft_type="Airbus A320",
        price=189.99,
        available_seats=90,
        total_seats=120,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF005",
        departure_airport="BAH",
        arrival_airport="KWI",
        departure_time=datetime.now() + timedelta(days=5, hours=12),
        arrival_time=datetime.now() + timedelta(days=5, hours=13),
        aircraft_type="Boeing 737",
        price=159.99,
        available_seats=60,
        total_seats=80,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF006",
        departure_airport="KWI",
        arrival_airport="BAH",
        departure_time=datetime.now() + timedelta(days=6, hours=18),
        arrival_time=datetime.now() + timedelta(days=6, hours=19),
        aircraft_type="Airbus A320",
        price=149.99,
        available_seats=70,
        total_seats=100,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF007",
        departure_airport="BAH",
        arrival_airport="CAI",
        departure_time=datetime.now() + timedelta(days=7, hours=6),
        arrival_time=datetime.now() + timedelta(days=7, hours=9),
        aircraft_type="Boeing 777",
        price=399.99,
        available_seats=200,
        total_seats=250,
        status="scheduled"
    ),
    FlightModel(
        flight_number="GF008",
        departure_airport="CAI",
        arrival_airport="BAH",
        departure_time=datetime.now() + timedelta(days=8, hours=20),
        arrival_time=datetime.now() + timedelta(days=8, hours=23),
        aircraft_type="Boeing 777",
        price=389.99,
        available_seats=180,
        total_seats=250,
        status="scheduled"
    )
    ]

flights_list = create_flights()
