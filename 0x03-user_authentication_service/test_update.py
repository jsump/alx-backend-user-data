from db import DB
from user import User

def test_update_user():
    # Initialize the database
    db = DB()

    # Add a new user to the database
    new_user = db.add_user(email="test@example.com", hashed_password="password123")

    # Update the user's attributes
    updated_attributes = {"email": "updated_test@example.com", "hashed_password": "updated_password123"}
    db.update_user(user_id=new_user.id, **updated_attributes)

    # Retrieve the user from the database
    updated_user = db.find_user_by(id=new_user.id)

    # Verify that the user's attributes are updated correctly
    assert updated_user.email == updated_attributes["email"]
    assert updated_user.hashed_password == updated_attributes["hashed_password"]

if __name__ == "__main__":
  test_update_user()
