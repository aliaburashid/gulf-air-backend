# =============================================================================
# OPENFLIGHTS DATA PROCESSOR - Downloads and processes real aviation data
# =============================================================================
# This module downloads real aviation data from OpenFlights.org database
# It provides authentic airport, airline, and route information for Gulf Air
# The data is used to create realistic flight schedules and destinations

import requests
import csv
import io
from typing import List, Dict, Optional

def download_openflights_data():
    """Download OpenFlights data from their repository
    
    Downloads three main datasets:
    - airports.dat: 10,000+ airports worldwide with codes and locations
    - airlines.dat: 6,000+ airlines with IATA/ICAO codes and details
    - routes.dat: 67,000+ flight routes between airports
    
    Returns:
        tuple: (airports_data, airlines_data, routes_data) as lists of dictionaries
    """
    
    # =============================================================================
    # DATA SOURCES - OpenFlights GitHub repository URLs
    # These URLs point to the official OpenFlights data files
    # The data is updated regularly and provides comprehensive aviation information
    # =============================================================================
    
    airports_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    airlines_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat"
    routes_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
    
    print("Downloading OpenFlights data...")
    
    # =============================================================================
    # AIRPORTS DATA PROCESSING - Parse airport information
    # Downloads and processes airport data from OpenFlights
    # Converts CSV format to structured dictionaries for easy access
    # =============================================================================
    
    # Download airports data
    airports_response = requests.get(airports_url)
    airports_data = []
    if airports_response.status_code == 200:
        airports_csv = csv.reader(io.StringIO(airports_response.text))
        for row in airports_csv:
            if len(row) >= 14:  # Ensure we have all required fields
                airports_data.append({
                    'id': row[0],           # Unique airport ID
                    'name': row[1],         # Full airport name
                    'city': row[2],         # City where airport is located
                    'country': row[3],      # Country where airport is located
                    'iata': row[4] if row[4] != '\\N' else None,  # 3-letter IATA code (e.g., "BAH")
                    'icao': row[5] if row[5] != '\\N' else None,  # 4-letter ICAO code (e.g., "OBBI")
                    'latitude': row[6],     # Geographic latitude
                    'longitude': row[7],    # Geographic longitude
                    'altitude': row[8],     # Airport elevation in feet
                    'timezone': row[9],     # UTC timezone offset
                    'dst': row[10],         # Daylight saving time rules
                    'tz_database': row[11], # Timezone database name
                    'type': row[12],        # Airport type (airport, heliport, etc.)
                    'source': row[13]       # Data source
                })
    
    # =============================================================================
    # AIRLINES DATA PROCESSING - Parse airline information
    # Downloads and processes airline data from OpenFlights
    # This helps us identify Gulf Air and other airlines in the system
    # =============================================================================m
    
    # Download airlines data
    airlines_response = requests.get(airlines_url)
    airlines_data = []
    if airlines_response.status_code == 200:
        airlines_csv = csv.reader(io.StringIO(airlines_response.text))
        for row in airlines_csv:
            if len(row) >= 8:
                airlines_data.append({
                    'id': row[0],           # Unique airline ID
                    'name': row[1],         # Full airline name (e.g., "Gulf Air")
                    'alias': row[2],        # Alternative name or alias
                    'iata': row[3] if row[3] != '\\N' else None,  # 2-letter IATA code (e.g., "GF")
                    'icao': row[4] if row[4] != '\\N' else None,  # 3-letter ICAO code (e.g., "GFA")
                    'callsign': row[5],     # Radio callsign (e.g., "GULF AIR")
                    'country': row[6],      # Country of origin (e.g., "Bahrain")
                    'active': row[7]        # Active status (Y/N)
                })
    
    # =============================================================================
    # ROUTES DATA PROCESSING - Parse flight route information
    # Downloads and processes route data from OpenFlights
    # This contains all the flight routes that airlines actually operate
    # =============================================================================
    
    # Download routes data
    routes_response = requests.get(routes_url)
    routes_data = []
    if routes_response.status_code == 200:
        routes_csv = csv.reader(io.StringIO(routes_response.text))
        for row in routes_csv:
            if len(row) >= 9:
                routes_data.append({
                    'airline': row[0],           # Airline IATA code (e.g., "GF")
                    'airline_id': row[1],        # Airline ID number
                    'source_airport': row[2],    # Departure airport IATA code (e.g., "BAH")
                    'source_airport_id': row[3], # Departure airport ID
                    'destination_airport': row[4], # Arrival airport IATA code (e.g., "LHR")
                    'destination_airport_id': row[5], # Arrival airport ID
                    'codeshare': row[6],         # Codeshare agreement (Y/N)
                    'stops': row[7],             # Number of stops (0 = direct, 1 = 1 stop, etc.)
                    'equipment': row[8]          # Aircraft type used (e.g., "Boeing 787")
                })
    
    return airports_data, airlines_data, routes_data

# =============================================================================
# GULF AIR ROUTE FILTER - Extract Gulf Air specific routes
# This function finds Gulf Air in the airlines database and extracts all routes
# that Gulf Air actually operates, providing authentic flight destinations
# =============================================================================

def get_gulf_air_routes(routes_data: List[Dict], airlines_data: List[Dict]) -> List[Dict]:
    """Filter routes for Gulf Air (GF)
    
    Args:
        routes_data: List of all flight routes from OpenFlights
        airlines_data: List of all airlines from OpenFlights
        
    Returns:
        List of routes that Gulf Air operates
    """

    
    gulf_air = None
    for airline in airlines_data:
        if airline.get('iata') == 'GF' or 'gulf air' in airline.get('name', '').lower():
            gulf_air = airline
            break
    
    if not gulf_air:
        print("Gulf Air not found in airlines data")
        return []
    
    print(f"Found Gulf Air: {gulf_air['name']} (IATA: {gulf_air['iata']})")
    
    # Match routes by airline IATA code or airline ID to get Gulf Air's actual routes
    
    gulf_air_routes = []
    for route in routes_data:
        if route.get('airline') == gulf_air['iata'] or route.get('airline_id') == gulf_air['id']:
            gulf_air_routes.append(route)
    
    return gulf_air_routes


# This function creates a lookup dictionary for airports by their IATA codes
# Makes it easy to find airport information when processing routes

def get_airports_by_codes(airports_data: List[Dict], codes: List[str]) -> Dict[str, Dict]:
    """Get airport information by IATA codes
    
    Args:
        airports_data: List of all airports from OpenFlights
        codes: List of IATA codes to look up (e.g., ["BAH", "LHR", "CDG"])
        
    Returns:
        Dictionary mapping IATA codes to airport information
    """
    airports_dict = {}
    for airport in airports_data:
        if airport.get('iata') in codes:
            airports_dict[airport['iata']] = airport
    return airports_dict


# This is the main function that orchestrates the entire data processing workflow
# Downloads OpenFlights data, filters for Gulf Air, and creates structured route information

def process_gulf_air_data():
    """Main function to process OpenFlights data for Gulf Air
    
    This function:
    1. Downloads all OpenFlights data (airports, airlines, routes)
    2. Filters for Gulf Air specific routes
    3. Extracts airport information for route endpoints
    4. Creates structured route data with full airport details
    
    Returns:
        List of processed Gulf Air routes with complete airport information
    """
    
    # STEP 1: DOWNLOAD DATA - Get all OpenFlights data
    airports_data, airlines_data, routes_data = download_openflights_data()
    
    # STEP 2: Find Gulf Air in the airlines database and get all their route 
    gulf_air_routes = get_gulf_air_routes(routes_data, airlines_data)
    print(f"Found {len(gulf_air_routes)} Gulf Air routes")
    
    # STEP 3:  Collect all unique airport codes (source and destination) from Gulf Air routes
    airport_codes = set()
    for route in gulf_air_routes:
        if route.get('source_airport'):
            airport_codes.add(route['source_airport'])
        if route.get('destination_airport'):
            airport_codes.add(route['destination_airport'])
    
    # STEP 4: Create a lookup dictionary for all airports used in Gulf Air routes   
    airports_dict = get_airports_by_codes(airports_data, list(airport_codes))
 
    # STEP 5: Combine route information with airport details to create complete route data
    processed_routes = []
    for route in gulf_air_routes[:20]:  # Limit to first 20 routes for demo
        source_airport = airports_dict.get(route.get('source_airport'))
        dest_airport = airports_dict.get(route.get('destination_airport'))
        
        if source_airport and dest_airport:
            processed_routes.append({
                'source_airport_code': route.get('source_airport'),      # IATA code (e.g., "BAH")
                'source_airport_name': source_airport.get('name'),       # Full name (e.g., "Bahrain International Airport")
                'source_city': source_airport.get('city'),               # City (e.g., "Manama")
                'source_country': source_airport.get('country'),         # Country (e.g., "Bahrain")
                'destination_airport_code': route.get('destination_airport'),  # IATA code (e.g., "LHR")
                'destination_airport_name': dest_airport.get('name'),    # Full name (e.g., "London Heathrow Airport")
                'destination_city': dest_airport.get('city'),            # City (e.g., "London")
                'destination_country': dest_airport.get('country'),      # Country (e.g., "United Kingdom")
                'aircraft_type': route.get('equipment', 'Boeing 737'),   # Aircraft type (default if not specified)
                'stops': route.get('stops', '0')                         # Number of stops (0 = direct flight)
            })
    
    return processed_routes


# MAIN EXECUTION - Run the data processing when script is executed directly
if __name__ == "__main__":
    # Process Gulf Air data from OpenFlights
    routes = process_gulf_air_data()
    
    # Display results
    print(f"\nProcessed {len(routes)} Gulf Air routes:")
    for route in routes[:5]:  # Show first 5 routes as example
        print(f"{route['source_airport_code']} ({route['source_city']}) -> {route['destination_airport_code']} ({route['destination_city']}) - {route['aircraft_type']}")
