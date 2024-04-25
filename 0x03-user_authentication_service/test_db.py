from db import DB
from sqlalchemy.orm.exc import NoResultFound

def test_db_operations():
    # Initialize DB instance
    db = DB()

    # Test adding a user
    added_user = db.add_user(email="test@example.com", hashed_password="password123")
    assert added_user.email == "test@example.com"
    assert added_user.hashed_password == "password123"

    # Test finding the added user by email
    found_user = db.find_user_by(email="test@example.com")
    assert found_user is not None
    assert found_user.email == "test@example.com"
    assert found_user.hashed_password == "password123"

    # Test updating the user's attributes
    db.update_user(user_id=found_user.id, hashed_password="new_password")
    updated_user = db.find_user_by(email="test@example.com")
    assert updated_user.hashed_password == "new_password"

    print("All test cases passed successfully.")

if __name__ == "__main__":
    test_db_operations()
