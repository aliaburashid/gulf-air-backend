# data/user_data.py

from models.user import UserModel

def create_test_users():
    user1 = UserModel(
        username="admin_user", 
        email="admin@gulfair.com",
        first_name="Admin",
        last_name="User",
        phone_number="+97312345678"
    )
    user1.set_password("admin123")
    
    user2 = UserModel(
        username="john_doe", 
        email="john.doe@email.com",
        first_name="John",
        last_name="Doe",
        phone_number="+97387654321"
    )
    user2.set_password("password123")
    
    user3 = UserModel(
        username="sarah_ahmed", 
        email="sarah.ahmed@gmail.com",
        first_name="Sarah",
        last_name="Ahmed",
        phone_number="+97123456789"
    )
    user3.set_password("password123")
    
    user4 = UserModel(
        username="mohammed_ali", 
        email="mohammed.ali@gmail.com",
        first_name="Mohammed",
        last_name="Ali",
        phone_number="+96612345678"
    )
    user4.set_password("password123")
    
    user5 = UserModel(
        username="fatima_hassan", 
        email="fatima.hassan@gmail.com",
        first_name="Fatima",
        last_name="Hassan",
        phone_number="+97412345678"
    )
    user5.set_password("password123")

    return [user1, user2, user3, user4, user5]

user_list = create_test_users()
