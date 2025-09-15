"""
Gulf Air Fleet Information
Based on official Gulf Air fleet data from https://www.gulfair.com/flying-with-us/our-fleet
"""

def get_gulf_air_fleet_details():
    """Returns detailed information about Gulf Air's current fleet"""
    
    return {
        "fleet_overview": {
            "total_aircraft": 45,
            "average_age": "7.8 years",
            "fleet_mix": "Modern wide-body and narrow-body aircraft",
            "environmental_focus": "Fuel-efficient next-generation aircraft"
        },
        
        "aircraft_details": [
            {
                "aircraft_type": "Boeing 787-9 Dreamliner",
                "quantity": 8,
                "configuration": "26 Falcon Gold + 256 Economy",
                "features": [
                    "Advanced aerodynamics",
                    "Fuel-efficient engines",
                    "Quieter cabin",
                    "Larger windows",
                    "Improved air quality"
                ],
                "routes": "Long-haul international routes",
                "introduced": "2018"
            },
            {
                "aircraft_type": "Airbus A321neo",
                "quantity": 8,
                "configuration": "16 Falcon Gold + 150 Economy",
                "features": [
                    "New Engine Option (neo)",
                    "Sharklet wingtips",
                    "Extended range capability",
                    "Higher passenger capacity"
                ],
                "routes": "Medium-haul routes",
                "introduced": "2020"
            },
            {
                "aircraft_type": "Airbus A321neo (HD)",
                "quantity": 4,
                "configuration": "12 Falcon Gold + 180 Economy",
                "features": [
                    "High-density configuration",
                    "Maximum passenger capacity",
                    "Fuel-efficient engines",
                    "Modern cabin design"
                ],
                "routes": "High-density medium-haul routes",
                "introduced": "2021"
            },
            {
                "aircraft_type": "Airbus A320neo",
                "quantity": 12,
                "configuration": "16 Falcon Gold + 120 Economy", 
                "features": [
                    "New Engine Option (neo)",
                    "Sharklet wingtips",
                    "Reduced noise levels",
                    "Lower emissions"
                ],
                "routes": "Regional and short-haul routes",
                "introduced": "2019"
            },
            {
                "aircraft_type": "Airbus A320neo (HD)",
                "quantity": 6,
                "configuration": "12 Falcon Gold + 138 Economy",
                "features": [
                    "High-density configuration",
                    "Optimized for short-haul",
                    "Fuel-efficient engines",
                    "Enhanced passenger experience"
                ],
                "routes": "High-density short-haul routes",
                "introduced": "2020"
            },
            {
                "aircraft_type": "Airbus A321ER",
                "quantity": 3,
                "configuration": "8 Falcon Gold + 161 Economy",
                "features": [
                    "Extended range capability",
                    "Long-range narrow-body",
                    "Fuel-efficient engines",
                    "Versatile route network"
                ],
                "routes": "Extended range medium-haul routes",
                "introduced": "2022"
            },
            {
                "aircraft_type": "Airbus A320-200",
                "quantity": 4,
                "configuration": "16 Falcon Gold + 120 Economy",
                "features": [
                    "Proven reliability",
                    "Classic A320 design",
                    "Efficient operations",
                    "Comfortable cabin"
                ],
                "routes": "Regional routes",
                "introduced": "2015"
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
        "short_haul": ["Airbus A320neo", "Airbus A320neo (HD)", "Airbus A320-200"],
        "medium_haul": ["Airbus A321neo", "Airbus A321neo (HD)", "Airbus A321ER"],
        "long_haul": ["Boeing 787-9 Dreamliner"],
        "high_density": ["Airbus A321neo (HD)", "Airbus A320neo (HD)"],
        "premium_routes": ["Boeing 787-9 Dreamliner"],
        "extended_range": ["Airbus A321ER", "Boeing 787-9 Dreamliner"]
    }
    
    return route_aircraft_mapping.get(route_type, ["Airbus A320neo"])

def get_seat_configuration(aircraft_type):
    """Returns seat configuration for specific aircraft type"""
    
    seat_configs = {
        "Boeing 787-9 Dreamliner": {
            "falcon_gold": {"seats": 26, "layout": "2-2-2"},
            "economy": {"seats": 256, "layout": "3-3-3"}
        },
        "Airbus A321neo": {
            "falcon_gold": {"seats": 16, "layout": "2-2"},
            "economy": {"seats": 150, "layout": "3-3"}
        },
        "Airbus A321neo (HD)": {
            "falcon_gold": {"seats": 12, "layout": "2-2"},
            "economy": {"seats": 180, "layout": "3-3"}
        },
        "Airbus A320neo": {
            "falcon_gold": {"seats": 16, "layout": "2-2"},
            "economy": {"seats": 120, "layout": "3-3"}
        },
        "Airbus A320neo (HD)": {
            "falcon_gold": {"seats": 12, "layout": "2-2"},
            "economy": {"seats": 138, "layout": "3-3"}
        },
        "Airbus A321ER": {
            "falcon_gold": {"seats": 8, "layout": "2-2"},
            "economy": {"seats": 161, "layout": "3-3"}
        },
        "Airbus A320-200": {
            "falcon_gold": {"seats": 16, "layout": "2-2"},
            "economy": {"seats": 120, "layout": "3-3"}
        }
    }
    
    return seat_configs.get(aircraft_type, seat_configs["Airbus A320neo"])
