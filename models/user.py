# Defines the User table structure and authentication methods

from sqlalchemy import Column, Integer, String
from .base import BaseModel
from passlib.context import CryptContext # Import new package
from datetime import datetime, timedelta, timezone  # New import for timestamps
import jwt  # New import for token generation
from config.environment import secret # Import the secret from the environment file
from sqlalchemy.orm import relationship

# Creating a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Inherits from BaseModel
class UserModel(BaseModel):
    
    # defines a user table in the database
    __tablename__ = "users"
    
    # user fields
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)  # Each username must be unique
    email = Column(String, unique=True)  # Each email must be unique
    password_hash = Column(String, nullable=True)  # Add new field for storing the hashed password
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

    # Relationships - a user can have multiple bookings
    bookings = relationship('BookingModel', back_populates='user')
    
    # Relationship to loyalty: Each user has one loyalty account
    loyalty = relationship('LoyaltyModel', back_populates='user', uselist=False)
    
    # password hashing: Takes a plain password and hashes it using bcrypt (passlib).
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    # Method to verify the password
    # Compares a plain password with the stored hash.
    # Returns True if it matches, False otherwise.
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
    
    # generates a JWT token
    def generate_token(self):        
        # Define the payload
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1), # Expiration time (1 day)
            "iat": datetime.now(timezone.utc), # Issued at time
            "sub": str(self.id), # Subject - the user ID
        }
        # Create the JWT token and encodes it using the secret key in environmnet.py
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token
