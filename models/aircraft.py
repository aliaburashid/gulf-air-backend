# =============================================================================
# AIRCRAFT MODEL - Stores information about Gulf Air's fleet
# =============================================================================
# This model stores details about each type of aircraft in Gulf Air's fleet
# It includes seat configurations, technical specifications, and performance data

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
    business_seats = Column(Integer)  # Business class seats
    first_seats = Column(Integer, default=0)  # First class seats (Gulf Air doesn't have first class)
    
    # Technical specifications
    range_km = Column(Integer)  # How far the aircraft can fly (kilometers)
    cruise_speed_kmh = Column(Integer)  # Normal flying speed (km/h)
    fuel_capacity_liters = Column(Integer)  # How much fuel it can carry
    
    # =============================================================================
    # GULF AIR FLEET DATA - Real aircraft specifications
    # =============================================================================
    # This method returns the actual aircraft types and specifications used by Gulf Air
    # Data is based on their official website and industry information
    
    @staticmethod
    def get_gulf_air_fleet():
        """Returns Gulf Air's simplified fleet specifications with only 2 aircraft types"""
        return [
            {
                'aircraft_type': 'Boeing 787 Dreamliner',
                'manufacturer': 'Boeing',
                'model': '787',
                'total_seats': 282,
                'economy_seats': 252,
                'business_seats': 30,
                'first_seats': 0,
                'range_km': 15750,
                'cruise_speed_kmh': 913,
                'fuel_capacity_liters': 126000
            },
            {
                'aircraft_type': 'Airbus A320',
                'manufacturer': 'Airbus',
                'model': 'A320',
                'total_seats': 144,
                'economy_seats': 132,
                'business_seats': 12,
                'first_seats': 0,
                'range_km': 6500,
                'cruise_speed_kmh': 840,
                'fuel_capacity_liters': 23800
            }
        ]
