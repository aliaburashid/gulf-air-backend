from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.flights import router as FlightsRouter
from controllers.bookings import router as BookingsRouter
from controllers.users import router as UsersRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'],
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
