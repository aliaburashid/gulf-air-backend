# seed.py

from sqlalchemy.orm import sessionmaker, Session
from config.environment import db_URI
from sqlalchemy import create_engine
from models.base import Base # import base model
# Import all models to ensure they are registered
from models.user import UserModel
from models.flight import FlightModel
from models.booking import BookingModel
from models.aircraft import AircraftModel

engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)

# This seed file is a separate program that can be used to "seed" our database with some initial data.
try:
    print("Recreating database...")
    # Dropping (or deleting) the tables and creating them again is for convenience. Once we start to play around with
    # our data, changing our models, this seed program will allow us to rapidly throw out the old data and replace it.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding the database...")
    db = SessionLocal()

    # Add users first (they are referenced by bookings)
    print("Adding users...")
    from data.user_data import user_list
    db.add_all(user_list)
    db.commit()

    # Add aircraft first (they are referenced by flights)
    print("Adding aircraft...")
    aircraft_list = []
    for aircraft_data in AircraftModel.get_gulf_air_fleet():
        aircraft = AircraftModel(**aircraft_data)
        aircraft_list.append(aircraft)
    db.add_all(aircraft_list)
    db.commit()

    # Add flights
    print("Adding flights...")
    from data.gulf_air_flights import flights_list
    db.add_all(flights_list)
    db.commit()

    # Add bookings (after users and flights are created)
    print("Adding bookings...")
    from data.booking_data import bookings_list
    db.add_all(bookings_list)
    db.commit()

    db.close()

    print("Database seeding complete! ✈️")
except Exception as e:
    print("An error occurred:", e)
