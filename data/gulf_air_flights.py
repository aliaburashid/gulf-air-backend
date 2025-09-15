# =============================================================================
# GULF AIR FLIGHTS DATA - Generates realistic flight data
# =============================================================================
# This file creates realistic Gulf Air flights using real route data from OpenFlights
# It includes proper pricing, aircraft assignments, and seat availability

from models.flight import FlightModel
from models.aircraft import AircraftModel
from datetime import datetime, timedelta
import random

def create_gulf_air_flights():
    """Create realistic Gulf Air flights using OpenFlights route data"""
    
    # =============================================================================
    # GULF AIR ROUTES - Real routes from OpenFlights database
    # =============================================================================
    # These are actual routes that Gulf Air operates, with real airport codes
    # Routes are organized by region for better organization
    
    gulf_air_routes = [
        # Middle East routes
        {"from": "BAH", "to": "DXB", "from_city": "Bahrain", "to_city": "Dubai"},
        {"from": "BAH", "to": "DOH", "from_city": "Bahrain", "to_city": "Doha"},
        {"from": "BAH", "to": "KWI", "from_city": "Bahrain", "to_city": "Kuwait"},
        {"from": "BAH", "to": "RUH", "from_city": "Bahrain", "to_city": "Riyadh"},
        {"from": "BAH", "to": "JED", "from_city": "Bahrain", "to_city": "Jeddah"},
        {"from": "BAH", "to": "CAI", "from_city": "Bahrain", "to_city": "Cairo"},
        {"from": "BAH", "to": "BEY", "from_city": "Bahrain", "to_city": "Beirut"},
        {"from": "BAH", "to": "AMM", "from_city": "Bahrain", "to_city": "Amman"},
        
        # European routes
        {"from": "BAH", "to": "LHR", "from_city": "Bahrain", "to_city": "London"},
        {"from": "BAH", "to": "CDG", "from_city": "Bahrain", "to_city": "Paris"},
        {"from": "BAH", "to": "FRA", "from_city": "Bahrain", "to_city": "Frankfurt"},
        {"from": "BAH", "to": "MAD", "from_city": "Bahrain", "to_city": "Madrid"},
        {"from": "BAH", "to": "FCO", "from_city": "Bahrain", "to_city": "Rome"},
        {"from": "BAH", "to": "ATH", "from_city": "Bahrain", "to_city": "Athens"},
        
        # Asian routes
        {"from": "BAH", "to": "BOM", "from_city": "Bahrain", "to_city": "Mumbai"},
        {"from": "BAH", "to": "DEL", "from_city": "Bahrain", "to_city": "Delhi"},
        {"from": "BAH", "to": "BKK", "from_city": "Bahrain", "to_city": "Bangkok"},
        {"from": "BAH", "to": "KUL", "from_city": "Bahrain", "to_city": "Kuala Lumpur"},
        {"from": "BAH", "to": "SIN", "from_city": "Bahrain", "to_city": "Singapore"},
        {"from": "BAH", "to": "HKG", "from_city": "Bahrain", "to_city": "Hong Kong"},
        
        # African routes
        {"from": "BAH", "to": "NBO", "from_city": "Bahrain", "to_city": "Nairobi"},
        {"from": "BAH", "to": "JNB", "from_city": "Bahrain", "to_city": "Johannesburg"},
        {"from": "BAH", "to": "ADD", "from_city": "Bahrain", "to_city": "Addis Ababa"},
    ]
    
    # =============================================================================
    # AIRCRAFT TYPES - Gulf Air's current fleet specifications
    # =============================================================================
    # These match the actual aircraft types in Gulf Air's fleet
    # Each aircraft has different seat configurations for economy and business classes
    
    aircraft_types = [
        {"id": 1, "type": "Boeing 787-9 Dreamliner", "economy_seats": 256, "falcon_gold_seats": 26},
        {"id": 2, "type": "Airbus A321neo", "economy_seats": 150, "falcon_gold_seats": 16},
        {"id": 3, "type": "Airbus A321neo (HD)", "economy_seats": 180, "falcon_gold_seats": 12},
        {"id": 4, "type": "Airbus A320neo", "economy_seats": 120, "falcon_gold_seats": 16},
        {"id": 5, "type": "Airbus A320neo (HD)", "economy_seats": 138, "falcon_gold_seats": 12},
        {"id": 6, "type": "Airbus A321ER", "economy_seats": 161, "falcon_gold_seats": 8},
        {"id": 7, "type": "Airbus A320-200", "economy_seats": 120, "falcon_gold_seats": 16},
    ]
    
    # =============================================================================
    # FLIGHT GENERATION - Create realistic flight schedule
    # =============================================================================
    # Generate flights for the next 30 days with realistic scheduling
    
    flights = []
    flight_number = 1
    
    # Create flights for the next 30 days
    for day in range(30):
        current_date = datetime.now() + timedelta(days=day)
        
        # Create 2-4 flights per day (realistic frequency)
        daily_flights = random.randint(2, 4)
        
        for flight_idx in range(daily_flights):
            # Select random route from Gulf Air's network
            route = random.choice(gulf_air_routes)
            
            # =============================================================================
            # AIRCRAFT SELECTION - Choose appropriate aircraft for route
            # =============================================================================
            # Long-haul routes use wide-body aircraft (787)
            # Short-haul routes use narrow-body aircraft (A320, A321)
            
            if route["to"] in ["LHR", "CDG", "FRA", "BKK", "KUL", "SIN", "HKG", "JNB"]:
                # Long-haul routes use wide-body aircraft (787-9)
                aircraft = aircraft_types[0]  # Boeing 787-9 Dreamliner
            else:
                # Short/medium-haul routes use narrow-body aircraft
                aircraft = random.choice([aircraft_types[1], aircraft_types[2], aircraft_types[3], aircraft_types[4], aircraft_types[5], aircraft_types[6]])
            
            # =============================================================================
            # FLIGHT TIMING - Generate realistic departure and arrival times
            # =============================================================================
            # Departure times are between 6 AM and 11 PM with 15-minute intervals
            
            departure_hour = random.randint(6, 23)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_time = current_date.replace(hour=departure_hour, minute=departure_minute, second=0, microsecond=0)
            
            # Calculate arrival time based on actual flight duration
            flight_duration_hours = get_flight_duration(route["from"], route["to"])
            arrival_time = departure_time + timedelta(hours=flight_duration_hours)
            
            # =============================================================================
            # PRICING LOGIC - Dynamic pricing based on route distance
            # =============================================================================
            # Economy and business class pricing with realistic ratios
            
            base_price = get_base_price(route["from"], route["to"])
            economy_price = base_price
            falcon_gold_price = base_price * 2.5  # Falcon Gold class is 2.5x economy price
            
            # =============================================================================
            # CREATE FLIGHT RECORD - Build the complete flight object
            # =============================================================================
            # This creates a complete flight with all necessary information
            
            flight = FlightModel(
                flight_number=f"GF{flight_number:03d}",  # Gulf Air flight numbers
                departure_airport=route["from"],  # Airport code
                arrival_airport=route["to"],      # Airport code
                departure_time=departure_time,    # When flight leaves
                arrival_time=arrival_time,        # When flight arrives
                aircraft_id=aircraft["id"],       # Which aircraft to use
                economy_price=economy_price,      # Economy class price
                falcon_gold_price=falcon_gold_price,    # Falcon Gold class price
                available_economy_seats=aircraft["economy_seats"],  # Starting economy seats
                available_falcon_gold_seats=aircraft["falcon_gold_seats"],
                status="scheduled"
            )
            
            flights.append(flight)
            flight_number += 1
    
    return flights

# =============================================================================
# HELPER FUNCTIONS - Support functions for flight generation
# =============================================================================

def get_flight_duration(departure_airport, arrival_airport):
    """Estimate flight duration based on route distance"""
    # This is a simplified calculation - in reality you'd use great circle distance
    # Routes are categorized by distance from Bahrain (BAH)
    
    # Short routes (Middle East) - 1.5-3 hours
    short_routes = ["DXB", "DOH", "KWI", "RUH", "JED", "CAI", "BEY", "AMM"]
    # Medium routes (Asia/Africa) - 4-7 hours  
    medium_routes = ["BOM", "DEL", "BKK", "KUL", "SIN", "HKG", "NBO", "ADD"]
    # Long routes (Europe) - 6-8 hours
    long_routes = ["LHR", "CDG", "FRA", "MAD", "FCO", "ATH", "JNB"]
    
    if arrival_airport in short_routes:
        return random.uniform(1.5, 3.0)  # 1.5-3 hours
    elif arrival_airport in medium_routes:
        return random.uniform(4.0, 7.0)  # 4-7 hours
    elif arrival_airport in long_routes:
        return random.uniform(6.0, 8.0)  # 6-8 hours
    else:
        return random.uniform(2.0, 4.0)  # Default 2-4 hours

def get_base_price(departure_airport, arrival_airport):
    """Generate base economy price based on route distance"""
    # This is a simplified pricing model - real airlines use complex algorithms
    # Prices are based on distance and market demand
    
    # Short routes (Middle East) - $150-300
    short_routes = ["DXB", "DOH", "KWI", "RUH", "JED", "CAI", "BEY", "AMM"]
    # Medium routes (Asia/Africa) - $300-600
    medium_routes = ["BOM", "DEL", "BKK", "KUL", "SIN", "HKG", "NBO", "ADD"]
    # Long routes (Europe) - $600-1200
    long_routes = ["LHR", "CDG", "FRA", "MAD", "FCO", "ATH", "JNB"]
    
    if arrival_airport in short_routes:
        return random.uniform(150, 300)  # $150-300
    elif arrival_airport in medium_routes:
        return random.uniform(300, 600)  # $300-600
    elif arrival_airport in long_routes:
        return random.uniform(500, 1000)  # $500-1000
    else:
        return random.uniform(200, 400)  # Default $200-400

# Create the flights list
flights_list = create_gulf_air_flights()
