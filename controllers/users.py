from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.user import UserModel
from serializers.user import UserSchema, UserToken, UserLogin, UserResponseSchema
from database import get_db

# Create a router for user-related endpoints
router = APIRouter()

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
        phone_number=user.phone_number
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

    # Find the user by username
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    # If user not found or password incorrect => throw error
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

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
