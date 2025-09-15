# =============================================================================
# LOYALTY POINTS MODEL - Gulf Air Falcon Flyer loyalty program
# This model tracks user loyalty points, tier status, and tier benefits
# Implements Gulf Air's real loyalty program with Blue, Silver, Gold, and Black tiers
# =============================================================================

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import BaseModel

class LoyaltyModel(BaseModel):
    """Loyalty points and tier tracking for Gulf Air Falcon Flyer program"""
    __tablename__ = "loyalty"
    
    id = Column(Integer, primary_key=True, index=True)  # Unique loyalty record ID
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)  # Links to user account
    
    # Membership status
    is_falcon_flyer_member = Column(String, default="inactive")  # "active", "inactive", "pending"
    membership_enrolled_date = Column(DateTime)  # When user joined Falcon Flyer
    
    # Current loyalty status
    current_tier = Column(String, default="Blue")  # Blue, Silver, Gold, Black
    total_points = Column(Integer, default=0)  # Lifetime points earned
    available_points = Column(Integer, default=0)  # Points available to spend
    
    # Tier tracking
    tier_achieved_date = Column(DateTime)  # When current tier was achieved
    tier_expiry_date = Column(DateTime)  # When tier expires (for Silver, Gold, Black)
    points_earned_this_period = Column(Integer, default=0)  # Points earned in current tier period
    
    # Relationship to user
    user = relationship('UserModel', back_populates='loyalty')
    
    
    @staticmethod
    def get_tier_requirements():
        """Returns Gulf Air's official loyalty tier requirements"""
        return {
            "Blue": {
                "points_required": 0,
                "validity_years": None,  # No expiry
                "renewal_points": 0,
                "description": "Entry level - default tier for all members"
            },
            "Silver": {
                "points_required": 900,
                "validity_years": 1,
                "renewal_points": 650,
                "description": "Silver tier - 1 year validity, 650 points to renew"
            },
            "Gold": {
                "points_required": 2500,
                "validity_years": 2,
                "renewal_points": 1750,
                "description": "Gold tier - 2 year validity, 1,750 points to retain"
            },
            "Black": {
                "points_required": 6500,
                "validity_years": 2,
                "renewal_points": 4550,
                "description": "Black tier - 2 year validity, 4,550 points to retain"
            }
        }
    
    @staticmethod
    def get_tier_benefits():
        """Returns benefits for each loyalty tier"""
        return {
            "Blue": {
                "priority_boarding": False,
                "extra_baggage": "0 kg",
                "lounge_access": False,
                "seat_selection": "Standard",
                "upgrade_eligibility": False,
                "points_bonus": "1x"
            },
            "Silver": {
                "priority_boarding": True,
                "extra_baggage": "10 kg",
                "lounge_access": False,
                "seat_selection": "Preferred",
                "upgrade_eligibility": True,
                "points_bonus": "1.25x"
            },
            "Gold": {
                "priority_boarding": True,
                "extra_baggage": "20 kg",
                "lounge_access": True,
                "seat_selection": "Preferred",
                "upgrade_eligibility": True,
                "points_bonus": "1.5x"
            },
            "Black": {
                "priority_boarding": True,
                "extra_baggage": "30 kg",
                "lounge_access": True,
                "seat_selection": "Premium",
                "upgrade_eligibility": True,
                "points_bonus": "2x"
            }
        }
    
    def calculate_tier_from_points(self, points: int) -> str:
        """Calculate tier based on total points earned"""
        requirements = self.get_tier_requirements()
        
        if points >= requirements["Black"]["points_required"]:
            return "Black"
        elif points >= requirements["Gold"]["points_required"]:
            return "Gold"
        elif points >= requirements["Silver"]["points_required"]:
            return "Silver"
        else:
            return "Blue"
    
    def get_points_bonus_multiplier(self) -> float:
        """Get points bonus multiplier for current tier"""
        benefits = self.get_tier_benefits()
        bonus_str = benefits[self.current_tier]["points_bonus"]
        return float(bonus_str.replace("x", ""))
    
    def get_benefits(self) -> dict:
        """Get all benefits for current tier"""
        return self.get_tier_benefits()[self.current_tier]
    
    def is_active_member(self) -> bool:
        """Check if user is an active Falcon Flyer member"""
        return self.is_falcon_flyer_member == "active"
    
    def enroll_in_falcon_flyer(self):
        """Enroll user in Falcon Flyer program"""
        from datetime import datetime
        self.is_falcon_flyer_member = "active"
        self.membership_enrolled_date = datetime.now()
        self.current_tier = "Blue"
        self.tier_achieved_date = datetime.now()
