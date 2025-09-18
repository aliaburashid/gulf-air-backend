from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.user import UserModel
from serializers.user import UserSchema, UserToken, UserLogin, UserResponseSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from pydantic import BaseModel

# Create a router for user-related endpoints
router = APIRouter()

# Pydantic model for loyalty data response
class LoyaltyData(BaseModel):
    loyalty_miles: int
    loyalty_points: int
    loyalty_tier: str
    membership_number: str
    first_name: str
    last_name: str

# ------------------------
# User Registration (Signup)
# ------------------------
@router.post("/register", response_model=UserResponseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create a new user object
    new_user = UserModel(
        username=user.username, 
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number or None  # Handle optional phone number
    )
    # Use the set_password method to hash the password before saving
    new_user.set_password(user.password)
    
    # Save user in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user # Response will hide the password (using schema)


# ------------------------
# User Login (Authentication)
# ------------------------
@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    # Validate that at least one identifier is provided
    if not any([user.email, user.falcon_flyer_number, user.username]):
        raise HTTPException(status_code=400, detail="Please provide email, Falcon Flyer number, or username")
    
    # Find the user by email, Falcon Flyer number, or username
    db_user = None
    
    if user.email:
        # Login with email
        db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    elif user.falcon_flyer_number:
        # Login with Falcon Flyer number (using username field for now)
        # In a real app, you'd have a separate Falcon Flyer number field
        db_user = db.query(UserModel).filter(UserModel.username == user.falcon_flyer_number).first()
    elif user.username:
        # Login with username
        db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate JWT token
    token = db_user.generate_token()

    # Return token and a success message
    return {"token": token, "message": "Login successful"}


# ------------------------
# Get all users
# ------------------------
@router.get('/users', response_model=List[UserResponseSchema])
def get_users(db: Session=Depends(get_db)):
    users = db.query(UserModel).all()
    return users


# ------------------------
# Get a single user by ID
# ------------------------
@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------------
# Get current user's loyalty data
# ------------------------
@router.get("/loyalty", response_model=LoyaltyData)
def get_loyalty_data(current_user: UserModel = Depends(get_current_user)):
    """Get the current user's Falconflyer loyalty program data"""
    return LoyaltyData(
        loyalty_miles=current_user.loyalty_miles or 0,
        loyalty_points=current_user.loyalty_points or 0,
        loyalty_tier=current_user.loyalty_tier or "BLUE",
        membership_number=current_user.membership_number or "N/A",
        first_name=current_user.first_name or "",
        last_name=current_user.last_name or ""
    )
