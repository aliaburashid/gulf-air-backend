# data/booking_data.py
from models.booking import BookingModel
from datetime import datetime, timedelta

def create_bookings():
    # Create some sample bookings
    return [
    BookingModel(
        booking_reference="GA12345678",
        user_id=2,
        flight_id=1,
        passenger_name="John Doe",
        passenger_email="john.doe@email.com",
        passport_number="2456176",
        seat_class="economy",
        seat_number="12A",
        booking_status="confirmed",
        total_price=299.99,
        booking_date=datetime.now() - timedelta(days=1)
    ),
    BookingModel(
        booking_reference="GA87654321",
        user_id=3,
        flight_id=2,
        passenger_name="Sarah Ahmed",
        passenger_email="sarah.ahmed@mail.ae",
        passport_number="33567890",
        seat_class="business",
        seat_number="8B",
        booking_status="confirmed",
        total_price=279.99,
        booking_date=datetime.now() - timedelta(days=2)
    ),
    BookingModel(
        booking_reference="GA11223344",
        user_id=4,
        flight_id=3,
        passenger_name="Mohammed Ali",
        passenger_email="mohammed.ali@correo.sa",
        passport_number="12233445",
        seat_class="economy",
        seat_number="15C",
        booking_status="confirmed",
        total_price=199.99,
        booking_date=datetime.now() - timedelta(days=3)
    )
    ]

bookings_list = create_bookings()
