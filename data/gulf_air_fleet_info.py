"""
Gulf Air Fleet Information
Based on official Gulf Air fleet data from https://www.gulfair.com/flying-with-us/our-fleet
"""

def get_gulf_air_fleet_details():
    """Returns detailed information about Gulf Air's current fleet"""
    
    return {
        "fleet_overview": {
            "total_aircraft": 20,
            "average_age": "6.5 years",
            "fleet_mix": "Simplified fleet with Boeing 787 and Airbus A320",
            "environmental_focus": "Fuel-efficient next-generation aircraft"
        },
        
        "aircraft_details": [
            {
                "aircraft_type": "Boeing 787 Dreamliner",
                "quantity": 10,
                "configuration": "30 Business + 252 Economy",
                "features": [
                    "Advanced aerodynamics",
                    "Fuel-efficient engines",
                    "Quieter cabin",
                    "Larger windows",
                    "Improved air quality",
                    "Dreamliner technology",
                    "Enhanced passenger comfort",
                    "Reduced jet lag"
                ],
                "routes": "Long-haul international routes",
                "introduced": "2016"
            },
            {
                "aircraft_type": "Airbus A320",
                "quantity": 10,
                "configuration": "12 Business + 132 Economy", 
                "features": [
                    "New Engine Option (neo)",
                    "Sharklet wingtips",
                    "Reduced noise levels",
                    "Lower emissions",
                    "Fuel-efficient engines",
                    "Modern cabin design"
                ],
                "routes": "Regional and short-haul routes",
                "introduced": "2019"
            }
        ],
        
        "fleet_highlights": [
            "One of the youngest fleets in the Middle East",
            "Focus on fuel efficiency and environmental responsibility",
            "Modern aircraft with latest technology",
            "Consistent passenger experience across fleet",
            "Regular fleet renewal program"
        ],
        
        "environmental_commitment": {
            "fuel_efficiency": "Up to 20% more fuel efficient than previous generation",
            "emissions_reduction": "Significantly reduced CO2 emissions",
            "noise_reduction": "Quieter aircraft for communities",
            "sustainability": "Part of Gulf Air's environmental strategy"
        }
    }

def get_aircraft_by_route_type(route_type):
    """Returns appropriate aircraft for different route types"""
    
    route_aircraft_mapping = {
        "short_haul": ["Airbus A320"],
        "medium_haul": ["Airbus A320"],
        "long_haul": ["Boeing 787 Dreamliner"],
        "high_density": ["Boeing 787 Dreamliner"],
        "premium_routes": ["Boeing 787 Dreamliner"]
    }
    
    return route_aircraft_mapping.get(route_type, ["Airbus A320"])

def get_seat_configuration(aircraft_type):
    """Returns seat configuration for specific aircraft type"""
    
    seat_configs = {
        "Boeing 787 Dreamliner": {
            "business": {"seats": 30, "layout": "2-2-2"},
            "economy": {"seats": 252, "layout": "3-3-3"}
        },
        "Airbus A320": {
            "business": {"seats": 12, "layout": "2-2"},
            "economy": {"seats": 132, "layout": "3-3"}
        }
    }
    
    return seat_configs.get(aircraft_type, seat_configs["Airbus A320"])
