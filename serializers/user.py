from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    
    class Config:
        orm_mode = True  # Enables compatibility with ORM models

# Schema for returning user data (without exposing the password)
class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True

# New schema for user login (supports email, username, or Falcon Flyer number)
class UserLogin(BaseModel):
    email: Optional[str] = None  # Email for email login
    falcon_flyer_number: Optional[str] = None  # Falcon Flyer number for loyalty login
    username: Optional[str] = None  # Username for traditional login
    password: str  # Plain text password provided by the user during login

# New schema for the response (containing the JWT token and a success message)
class UserToken(BaseModel):
    token: str  # JWT token generated upon successful login
    message: str  # Success message

    class Config:
        orm_mode = True
