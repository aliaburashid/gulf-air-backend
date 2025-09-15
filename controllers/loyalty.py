# =============================================================================
# LOYALTY CONTROLLER - Gulf Air Falcon Flyer loyalty program endpoints
# This controller handles all loyalty program operations including:
# - Viewing loyalty status and benefits
# - Earning points from bookings
# - Tier upgrades and renewals
# - Points redemption
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.loyalty import LoyaltyModel
from models.user import UserModel
from models.booking import BookingModel
from serializers.loyalty import (
    LoyaltySchema, LoyaltyBenefits, LoyaltyTierInfo, 
    PointsTransaction, LoyaltySummary, FalconFlyerEnrollment
)
from database import get_db
from dependencies.get_current_user import get_current_user
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

# =============================================================================
# GET LOYALTY STATUS - View user's loyalty program status
# Users can view their current tier, points, and benefits
# =============================================================================

@router.get("/loyalty/status", response_model=LoyaltySummary)
def get_loyalty_status(
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    """Get user's complete loyalty program status"""
    
    # Get or create loyalty account
    loyalty = db.query(LoyaltyModel).filter(LoyaltyModel.user_id == current_user.id).first()
    if not loyalty:
        # Create new loyalty account for user (inactive by default)
        loyalty = LoyaltyModel(
            user_id=current_user.id,
            is_falcon_flyer_member="inactive",
            current_tier="Blue",
            total_points=0,
            available_points=0
        )
        db.add(loyalty)
        db.commit()
        db.refresh(loyalty)
    
    # Calculate points to next tier
    requirements = LoyaltyModel.get_tier_requirements()
    current_tier_index = list(requirements.keys()).index(loyalty.current_tier)
    next_tier = None
    points_to_next = 0
    
    if current_tier_index < len(requirements) - 1:
        next_tier = list(requirements.keys())[current_tier_index + 1]
        next_tier_requirement = requirements[next_tier]["points_required"]
        points_to_next = next_tier_requirement - loyalty.total_points
    
    # Get current tier benefits
    benefits = loyalty.get_benefits()
    tier_benefits = LoyaltyBenefits(
        tier=loyalty.current_tier,
        **benefits
    )
    
    return LoyaltySummary(
        is_falcon_flyer_member=loyalty.is_falcon_flyer_member,
        membership_enrolled_date=loyalty.membership_enrolled_date,
        current_tier=loyalty.current_tier,
        total_points=loyalty.total_points,
        available_points=loyalty.available_points,
        points_to_next_tier=points_to_next,
        next_tier=next_tier,
        tier_benefits=tier_benefits,
        tier_expiry=loyalty.tier_expiry_date,
        points_this_period=loyalty.points_earned_this_period
    )

# =============================================================================
# GET ALL TIER INFORMATION - View all loyalty tiers and requirements
# Users can see what benefits each tier offers and requirements
# =============================================================================

@router.get("/loyalty/tiers", response_model=List[LoyaltyTierInfo])
def get_all_tiers():
    """Get information about all loyalty tiers"""
    
    requirements = LoyaltyModel.get_tier_requirements()
    benefits = LoyaltyModel.get_tier_benefits()
    
    tier_info = []
    for tier_name, tier_req in requirements.items():
        tier_benefits = LoyaltyBenefits(tier=tier_name, **benefits[tier_name])
        tier_info.append(LoyaltyTierInfo(
            tier=tier_name,
            **tier_req,
            benefits=tier_benefits
        ))
    
    return tier_info

# =============================================================================
# JOIN FALCON FLYER - Enroll in the loyalty program
# Users must explicitly join to start earning points
# =============================================================================

@router.post("/loyalty/enroll")
def join_falcon_flyer(
    enrollment: FalconFlyerEnrollment,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Join the Falcon Flyer loyalty program"""
    
    if not enrollment.agree_to_terms:
        raise HTTPException(
            status_code=400, 
            detail="You must agree to the terms and conditions to join Falcon Flyer"
        )
    
    # Get or create loyalty account
    loyalty = db.query(LoyaltyModel).filter(LoyaltyModel.user_id == current_user.id).first()
    if not loyalty:
        loyalty = LoyaltyModel(
            user_id=current_user.id,
            is_falcon_flyer_member="inactive",
            current_tier="Blue",
            total_points=0,
            available_points=0
        )
        db.add(loyalty)
    
    # Check if already a member
    if loyalty.is_falcon_flyer_member == "active":
        raise HTTPException(
            status_code=400,
            detail="You are already a Falcon Flyer member"
        )
    
    # Enroll in Falcon Flyer
    loyalty.enroll_in_falcon_flyer()
    db.commit()
    db.refresh(loyalty)
    
    return {
        "message": "Welcome to Falcon Flyer! You can now start earning loyalty points.",
        "membership_status": "active",
        "current_tier": "Blue",
        "enrolled_date": loyalty.membership_enrolled_date
    }

# =============================================================================
# EARN POINTS - Award points to user (internal function)
# This function is called internally when users make bookings
# =============================================================================

def award_loyalty_points(
    user_id: int, 
    points: int, 
    reason: str, 
    db: Session
) -> dict:
    """Award loyalty points to a user (only if they're an active Falcon Flyer member)"""
    
    # Get or create loyalty account
    loyalty = db.query(LoyaltyModel).filter(LoyaltyModel.user_id == user_id).first()
    if not loyalty:
        # Create inactive loyalty account
        loyalty = LoyaltyModel(
            user_id=user_id,
            is_falcon_flyer_member="inactive",
            current_tier="Blue",
            total_points=0,
            available_points=0
        )
        db.add(loyalty)
    
    # Check if user is an active Falcon Flyer member
    if not loyalty.is_active_member():
        return {
            "points_earned": 0,
            "message": "You must be a Falcon Flyer member to earn loyalty points. Join now to start earning!",
            "membership_required": True
        }
    
    # Apply tier bonus multiplier
    bonus_multiplier = loyalty.get_points_bonus_multiplier()
    bonus_points = int(points * bonus_multiplier)
    total_points_earned = bonus_points
    
    # Update loyalty points
    loyalty.total_points += total_points_earned
    loyalty.available_points += total_points_earned
    loyalty.points_earned_this_period += total_points_earned
    
    # Check for tier upgrade
    new_tier = loyalty.calculate_tier_from_points(loyalty.total_points)
    if new_tier != loyalty.current_tier:
        loyalty.current_tier = new_tier
        loyalty.tier_achieved_date = datetime.now()
        
        # Set tier expiry date for non-Blue tiers
        requirements = LoyaltyModel.get_tier_requirements()
        if requirements[new_tier]["validity_years"]:
            loyalty.tier_expiry_date = datetime.now() + timedelta(
                years=requirements[new_tier]["validity_years"]
            )
    
    db.commit()
    db.refresh(loyalty)
    
    return {
        "points_earned": total_points_earned,
        "base_points": points,
        "bonus_multiplier": bonus_multiplier,
        "new_tier": loyalty.current_tier,
        "total_points": loyalty.total_points,
        "available_points": loyalty.available_points
    }

# =============================================================================
# CALCULATE BOOKING POINTS - Calculate points for a flight booking
# This function calculates how many points a user earns from a booking
# =============================================================================

def calculate_booking_points(booking: BookingModel, flight) -> int:
    """Calculate loyalty points earned from a flight booking"""
    
    # Base points calculation (1 point per BHD spent)
    base_points = int(booking.total_price)
    
    # Additional factors
    points = base_points
    
    # Long-haul bonus (flights over 4 hours)
    flight_duration = flight.arrival_time - flight.departure_time
    if flight_duration.total_seconds() > 4 * 3600:  # 4 hours
        points += int(base_points * 0.5)  # 50% bonus for long-haul
    
    # Falcon Gold class bonus
    if booking.seat_class == "falcon_gold":
        points += int(base_points * 0.25)  # 25% bonus for premium class
    
    return points

# =============================================================================
# GET LOYALTY HISTORY - View points earning history
# Users can see their points earning history from bookings
# =============================================================================

@router.get("/loyalty/history")
def get_loyalty_history(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get user's loyalty points earning history"""
    
    # Get user's bookings with flight information
    bookings = db.query(BookingModel).filter(
        BookingModel.user_id == current_user.id,
        BookingModel.booking_status == "confirmed"
    ).all()
    
    history = []
    for booking in bookings:
        # Calculate points for this booking
        flight = db.query(FlightModel).filter(FlightModel.id == booking.flight_id).first()
        if flight:
            points_earned = calculate_booking_points(booking, flight)
            history.append({
                "booking_reference": booking.booking_reference,
                "flight_number": flight.flight_number,
                "route": f"{flight.departure_airport} → {flight.arrival_airport}",
                "booking_date": booking.booking_date,
                "points_earned": points_earned,
                "seat_class": booking.seat_class,
                "total_price": booking.total_price
            })
    
    return {
        "total_bookings": len(history),
        "history": history
    }
