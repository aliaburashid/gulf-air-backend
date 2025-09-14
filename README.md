# Gulf Air Backend API

A FastAPI-based backend for Gulf Air flight booking system, built following the same structure as the Python FastAPI tea app.

## Project Structure

```
gulf-air-backend/
├── config/
│   └── environment.py          # Database URI and secret key configuration
├── controllers/
│   ├── users.py               # User authentication and management endpoints
│   ├── flights.py             # Flight management endpoints
│   └── bookings.py            # Booking management endpoints
├── data/
│   ├── user_data.py           # Sample user data for seeding
│   ├── flight_data.py         # Sample flight data for seeding
│   └── booking_data.py        # Sample booking data for seeding
├── dependencies/
│   └── get_current_user.py    # JWT authentication dependency
├── models/
│   ├── base.py                # Base model with common fields
│   ├── user.py                # User model with authentication
│   ├── flight.py              # Flight model
│   └── booking.py             # Booking model
├── serializers/
│   ├── user.py                # User request/response schemas
│   ├── flight.py              # Flight request/response schemas
│   └── booking.py             # Booking request/response schemas
├── database.py                # SQLAlchemy database configuration
├── main.py                    # FastAPI application entry point
├── seed.py                    # Database seeding script
├── Pipfile                    # Python dependencies
└── README.md                  # This file
```

## Features

- **User Management**: Registration, login, and JWT authentication
- **Flight Management**: CRUD operations for flights with search functionality
- **Booking Management**: Create, view, update, and cancel bookings
- **Authentication**: JWT-based authentication with password hashing
- **Database**: PostgreSQL with SQLAlchemy ORM
- **CORS**: Configured for frontend integration

## Setup Instructions

### 1. Install Dependencies

```bash
# Install pipenv if you haven't already
pip install pipenv

# Install project dependencies
pipenv install
```

### 2. Database Setup

Update the database URI in `config/environment.py`:

```python
db_URI="postgresql://username:password@localhost:5432/gulf_air_db"
```

Or use SQLite for development:

```python
db_URI="sqlite:///./gulf_air_db.db"
```

### 3. Seed the Database

```bash
# Activate the virtual environment
pipenv shell

# Run the seed script to create tables and add sample data
python seed.py
```

### 4. Run the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication (`/auth`)

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/users` - Get all users (admin only)
- `GET /auth/users/{user_id}` - Get user by ID

### Flights (`/api`)

- `GET /api/flights` - Get all flights
- `GET /api/flights/{flight_id}` - Get flight by ID
- `POST /api/flights` - Create new flight
- `PUT /api/flights/{flight_id}` - Update flight
- `DELETE /api/flights/{flight_id}` - Delete flight
- `GET /api/flights/search/{departure_airport}/{arrival_airport}` - Search flights

### Bookings (`/api`)

- `GET /api/bookings` - Get user's bookings (requires authentication)
- `GET /api/bookings/{booking_id}` - Get booking by ID
- `POST /api/bookings` - Create new booking (requires authentication)
- `PUT /api/bookings/{booking_id}` - Update booking
- `DELETE /api/bookings/{booking_id}` - Cancel booking
- `GET /api/bookings/reference/{booking_reference}` - Get booking by reference

## Sample Data

The seed script creates:

- **5 test users** with different roles and locations
- **8 sample flights** between major Gulf cities
- **3 sample bookings** for testing

### Test User Credentials

- Username: `admin_user`, Password: `admin123`
- Username: `john_doe`, Password: `password123`
- Username: `sarah_ahmed`, Password: `password123`

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Database Models

### User Model
- id, username, email, password_hash
- first_name, last_name, phone_number
- created_at, updated_at

### Flight Model
- id, flight_number, departure_airport, arrival_airport
- departure_time, arrival_time, aircraft_type
- price, available_seats, total_seats, status
- created_at, updated_at

### Booking Model
- id, booking_reference, user_id, flight_id
- passenger_name, passenger_email, seat_number
- booking_status, total_price, booking_date
- created_at, updated_at

## Development

To add new features:

1. Create/update models in `models/`
2. Create/update serializers in `serializers/`
3. Create/update controllers in `controllers/`
4. Add routes to `main.py`
5. Update seed data if needed

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
