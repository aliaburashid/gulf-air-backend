# =============================================================================
# AIRCRAFT MODEL - Stores information about Gulf Air's fleet
# This model stores details about each type of aircraft in Gulf Air's fleet
# It includes seat configurations, technical specifications, and performance data
# =============================================================================

from sqlalchemy import Column, Integer, String, Float
from .base import BaseModel

class AircraftModel(BaseModel):
    """Aircraft model with Gulf Air fleet specifications"""
    
    __tablename__ = "aircraft"  # Database table name
    
    # Basic aircraft identification
    id = Column(Integer, primary_key=True, index=True)  # Unique aircraft ID
    aircraft_type = Column(String, unique=True)  # Full name: "Boeing 787-9 Dreamliner"
    manufacturer = Column(String)  # Company: "Boeing", "Airbus", etc.
    model = Column(String)  # Model number: "787-9", "A320neo", etc.
    
    # Seat configuration - how many seats in each class
    total_seats = Column(Integer)  # Total passenger capacity
    economy_seats = Column(Integer)  # Economy class seats
    falcon_gold_seats = Column(Integer)  # Falcon Gold class seats (Gulf Air's premium class)
    first_seats = Column(Integer, default=0)  # First class seats (Gulf Air doesn't have first class)
    
    # Technical specifications
    range_km = Column(Integer)  # How far the aircraft can fly (kilometers)
    cruise_speed_kmh = Column(Integer)  # Normal flying speed (km/h)
    fuel_capacity_liters = Column(Integer)  # How much fuel it can carry
    
    # =============================================================================
    # GULF AIR FLEET DATA - Real aircraft specifications
    # This method returns the actual aircraft types and specifications used by Gulf Air
    # =============================================================================
    
    # it doesn't need any class or instance data.
    # It allows you to define utility functions inside a class without needing self
    @staticmethod
    def get_gulf_air_fleet():
        """Returns Gulf Air's current fleet specifications based on their official fleet page"""
        return [
            {
                'aircraft_type': 'Boeing 787-9 Dreamliner',
                'manufacturer': 'Boeing',
                'model': '787-9',
                'total_seats': 282,
                'economy_seats': 256,
                'falcon_gold_seats': 26,
                'first_seats': 0,
                'range_km': 15750,
                'cruise_speed_kmh': 913,
                'fuel_capacity_liters': 126000
            },
            {
                'aircraft_type': 'Airbus A321neo',
                'manufacturer': 'Airbus',
                'model': 'A321neo',
                'total_seats': 166,
                'economy_seats': 150,
                'falcon_gold_seats': 16,
                'first_seats': 0,
                'range_km': 6500,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            },
            {
                'aircraft_type': 'Airbus A321neo (HD)',
                'manufacturer': 'Airbus',
                'model': 'A321neo HD',
                'total_seats': 192,
                'economy_seats': 180,
                'falcon_gold_seats': 12,
                'first_seats': 0,
                'range_km': 6500,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            },
            {
                'aircraft_type': 'Airbus A320neo',
                'manufacturer': 'Airbus',
                'model': 'A320neo',
                'total_seats': 136,
                'economy_seats': 120,
                'falcon_gold_seats': 16,
                'first_seats': 0,
                'range_km': 6500,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            },
            {
                'aircraft_type': 'Airbus A320neo (HD)',
                'manufacturer': 'Airbus',
                'model': 'A320neo HD',
                'total_seats': 150,
                'economy_seats': 138,
                'falcon_gold_seats': 12,
                'first_seats': 0,
                'range_km': 6500,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            },
            {
                'aircraft_type': 'Airbus A321ER',
                'manufacturer': 'Airbus',
                'model': 'A321ER',
                'total_seats': 169,
                'economy_seats': 161,
                'falcon_gold_seats': 8,
                'first_seats': 0,
                'range_km': 7400,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            },
            {
                'aircraft_type': 'Airbus A320-200',
                'manufacturer': 'Airbus',
                'model': 'A320-200',
                'total_seats': 136,
                'economy_seats': 120,
                'falcon_gold_seats': 16,
                'first_seats': 0,
                'range_km': 6100,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            }
        ]
