# ✈️ Gulf Air App — Backend (FastAPI)

The engine powering the Gulf Air mobile app. Built with FastAPI + SQLAlchemy + SQLite, this backend handles authentication, flight data, bookings, seat management, and the Falconflyer loyalty programme.

---

## 🧰 Tech Stack

- **FastAPI** — modern Python web framework
- **SQLAlchemy** — ORM for database models
- **SQLite** — lightweight local database
- **Pydantic** — data validation
- **JWT** — authentication via PyJWT + Passlib
- **Uvicorn** — ASGI server

---

## 🗺️ Project Structure

```
gulf-air-backend/
├── config/
│   └── environment.py          # db_URI and secret key (not tracked in git)
├── controllers/
│   ├── users.py                # Auth + loyalty endpoints
│   ├── flights.py              # Flight endpoints + booked seats
│   └── bookings.py             # Booking endpoints
├── data/
│   ├── user_data.py
│   ├── gulf_air_flights.py
│   ├── gulf_air_fleet_info.py
│   └── booking_data.py
├── dependencies/
│   └── get_current_user.py
├── models/
│   ├── base.py
│   ├── user.py
│   ├── flight.py
│   ├── booking.py
│   └── aircraft.py
├── serializers/
│   ├── user.py
│   ├── flight.py
│   └── booking.py
├── database.py
├── main.py
├── seed.py
├── Pipfile
└── Pipfile.lock
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/aliaburashid/gulf-air-backend.git
cd gulf-air-backend
```

### 2. Create the config file

This file is not tracked in git — you must create it manually:

```bash
cat > config/environment.py << 'EOF'
db_URI = "sqlite:///./gulf_air.db"
SECRET_KEY = "supersecretkey123"
secret = "supersecretkey123"
EOF
```

### 3. Install dependencies

```bash
pip install pipenv
python3 -m pipenv --python /opt/homebrew/bin/python3.11
python3 -m pipenv install --dev
python3 -m pipenv run pip install PyJWT "bcrypt==4.0.1"
```

### 4. Seed the database

```bash
python3 -m pipenv run python seed.py
```

### 5. Start the server

```bash
python3 -m pipenv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Auth (`/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/users` | Get all users |
| GET | `/auth/users/{id}` | Get user by ID |
| GET | `/auth/loyalty` | Get loyalty data (auth required) |

### Flights (`/api`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/flights` | Get all flights |
| GET | `/api/flights/{id}` | Get flight by ID |
| GET | `/api/flights/{id}/booked-seats` | Get booked seats for a flight |
| GET | `/api/flights/search/{dep}/{arr}` | Search flights by route |
| GET | `/api/flights/status/{flight_number}` | Get flight status |
| POST | `/api/flights` | Create flight |
| PUT | `/api/flights/{id}` | Update flight |
| DELETE | `/api/flights/{id}` | Delete flight |

### Bookings (`/api`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings` | Get user's bookings (auth required) |
| POST | `/api/bookings` | Create booking (auth required) |
| GET | `/api/bookings/{id}` | Get booking by ID |
| PUT | `/api/bookings/{id}` | Update booking |
| DELETE | `/api/bookings/{id}` | Cancel booking |
| GET | `/api/bookings/reference/{ref}` | Get booking by reference |
| POST | `/api/bookings/{id}/reschedule` | Reschedule booking |
| POST | `/api/bookings/{id}/checkin` | Check in and earn miles |

---

## 🔐 Test Users

| Username | Password | Email |
|----------|----------|-------|
| aliaburashid | alia123 | burashidalia@gmail.com |
| admin_user | admin123 | admin@gulfair.com |
| john_doe | password123 | john@example.com |
| sarah_ahmed | password123 | sarah@example.com |

---

## 🏅 Falconflyer Loyalty Programme

Check-in calculates miles and points based on flight distance, seat class, and loyalty tier.

| Tier | Points Required |
|------|----------------|
| BLUE | 0 |
| SILVER | 500 |
| GOLD | 1,000 |
| PLATINUM | 2,000 |

Seat class multipliers: Economy 1.0x · Falcon Gold 1.5x

Tier multipliers: BLUE 1.0x · SILVER 1.25x · GOLD 1.5x · PLATINUM 2.0x

---

## ✈️ Gulf Air Fleet

| Aircraft | Business | Economy | Business Config | Economy Config |
|----------|----------|---------|----------------|----------------|
| Airbus A320 | 16 seats | 120 seats | 2+2 (A C / D F) | 3+3 (A B C / D E F) |
| Boeing 787 Dreamliner | 30 seats | 252 seats | 2+2+2 (A C / D G / H K) | 3+3+3 (A B C / D E F / G H K) |

---

## 🛟 Troubleshooting

- **`command not found: pipenv`** — use `python3 -m pipenv` instead
- **Port 8000 in use** — run `kill -9 $(lsof -t -i:8000)` then restart
- **`No module named config.environment`** — create the file manually (see step 2)
- **bcrypt errors** — install `bcrypt==4.0.1` specifically
- **Python version errors** — project requires Python 3.10+ for `str | None` syntax

---

## 📖 API Documentation

Once the server is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
