from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.flights import router as FlightsRouter
from controllers.bookings import router as BookingsRouter
from controllers.users import router as UsersRouter

# Import all models to ensure they're registered with SQLAlchemy
from models.user import UserModel
from models.flight import FlightModel
from models.booking import BookingModel
from models.aircraft import AircraftModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins for mobile development
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(FlightsRouter, prefix='/api')
app.include_router(BookingsRouter, prefix='/api')
app.include_router(UsersRouter, prefix='/auth')

@app.get('/')
def home():
    return {'message': 'Welcome to Gulf Air API!'}
