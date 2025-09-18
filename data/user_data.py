# data/user_data.py

from models.user import UserModel

def create_test_users():
    user1 = UserModel(
        username="admin_user", 
        email="admin@gulfair.com",
        first_name="Admin",
        last_name="User",
        phone_number="+97312345678",
        loyalty_miles=15000,
        loyalty_points=500,
        loyalty_tier="SILVER",
        membership_number="GF001234"
    )
    user1.set_password("admin123")
    
    user2 = UserModel(
        username="john_doe", 
        email="john.doe@email.com",
        first_name="John",
        last_name="Doe",
        phone_number="+97387654321",
        loyalty_miles=8500,
        loyalty_points=300,
        loyalty_tier="BLUE",
        membership_number="GF002345"
    )
    user2.set_password("password123")
    
    user3 = UserModel(
        username="sarah_ahmed", 
        email="sarah.ahmed@gmail.com",
        first_name="Sarah",
        last_name="Ahmed",
        phone_number="+97123456789",
        loyalty_miles=25000,
        loyalty_points=1200,
        loyalty_tier="GOLD",
        membership_number="GF003456"
    )
    user3.set_password("password123")
    
    user4 = UserModel(
        username="mohammed_ali", 
        email="mohammed.ali@gmail.com",
        first_name="Mohammed",
        last_name="Ali",
        phone_number="+96612345678",
        loyalty_miles=5000,
        loyalty_points=150,
        loyalty_tier="BLUE",
        membership_number="GF004567"
    )
    user4.set_password("password123")
    
    user5 = UserModel(
        username="aliaburashid", 
        email="burashidalia@gmail.com",
        first_name="Alia",
        last_name="Burashid",
        phone_number="+97333740073",
        loyalty_miles=27852,
        loyalty_points=700,
        loyalty_tier="BLUE",
        membership_number="GF82413429"
    )
    user5.set_password("alia123")

    return [user1, user2, user3, user4, user5]

user_list = create_test_users()
