# =============================================================================
# LOYALTY SERIALIZERS - Data validation for loyalty program operations
# =============================================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# =============================================================================
# LOYALTY SCHEMA - For reading loyalty information
# Used when returning loyalty data to users (points, tier, benefits)
# =============================================================================

class LoyaltySchema(BaseModel):
    """Loyalty information schema for API responses"""
    id: Optional[int] = Field(default=None)  # Loyalty record ID
    user_id: int  # User ID this loyalty account belongs to
    is_falcon_flyer_member: str  # Membership status: "active", "inactive", "pending"
    membership_enrolled_date: Optional[datetime] = None  # When user joined Falcon Flyer
    current_tier: str  # Current tier: Blue, Silver, Gold, Black
    total_points: int  # Lifetime points earned
    available_points: int  # Points available to spend
    tier_achieved_date: Optional[datetime] = None  # When current tier was achieved
    tier_expiry_date: Optional[datetime] = None  # When tier expires
    points_earned_this_period: int  # Points earned in current tier period
    
    class Config:
        orm_mode = True  # Allows working with database objects directly

# =============================================================================
# LOYALTY BENEFITS - Tier benefits information
# Used to show users what benefits they get with their current tier
# =============================================================================

class LoyaltyBenefits(BaseModel):
    """Loyalty tier benefits schema"""
    tier: str  # Tier name
    priority_boarding: bool  # Priority boarding access
    extra_baggage: str  # Extra baggage allowance
    lounge_access: bool  # Airport lounge access
    seat_selection: str  # Seat selection type
    upgrade_eligibility: bool  # Can be upgraded
    points_bonus: str  # Points earning multiplier

# =============================================================================
# LOYALTY TIER INFO - Complete tier information
# Used to show users tier requirements and benefits
# =============================================================================

class LoyaltyTierInfo(BaseModel):
    """Complete tier information including requirements and benefits"""
    tier: str  # Tier name
    points_required: int  # Points needed to reach this tier
    validity_years: Optional[int] = None  # How long tier is valid
    renewal_points: int  # Points needed to renew tier
    description: str  # Tier description
    benefits: LoyaltyBenefits  # Tier benefits

# =============================================================================
# POINTS TRANSACTION - For tracking points earned/spent
# Used when awarding or deducting loyalty points
# =============================================================================

class PointsTransaction(BaseModel):
    """Points transaction schema"""
    points: int  # Points to add/subtract (positive for earning, negative for spending)
    reason: str  # Reason for points transaction (e.g., "Flight booking", "Points redemption")
    description: Optional[str] = None  # Additional details about the transaction

# =============================================================================
# LOYALTY SUMMARY - User's complete loyalty status
# Used to show users their complete loyalty program status
# =============================================================================

class LoyaltySummary(BaseModel):
    """Complete loyalty status summary"""
    is_falcon_flyer_member: str  # Membership status
    membership_enrolled_date: Optional[datetime] = None  # When joined
    current_tier: str  # Current tier
    total_points: int  # Lifetime points
    available_points: int  # Spendable points
    points_to_next_tier: int  # Points needed for next tier
    next_tier: Optional[str] = None  # Next tier name
    tier_benefits: LoyaltyBenefits  # Current tier benefits
    tier_expiry: Optional[datetime] = None  # When current tier expires
    points_this_period: int  # Points earned in current tier period

# =============================================================================
# FALCON FLYER ENROLLMENT - For joining the loyalty program
# Used when users want to join the Falcon Flyer program
# =============================================================================

class FalconFlyerEnrollment(BaseModel):
    """Falcon Flyer enrollment request"""
    agree_to_terms: bool  # User must agree to terms and conditions
    marketing_communications: bool = False  # Optional marketing opt-in
