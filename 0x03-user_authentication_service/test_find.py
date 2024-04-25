from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def test_find_user_by():
    # Initialize DB instance
    db = DB()

    # Clear the database before running the test
    db._session.query(User).delete()
    db._session.commit()

    # Test finding user by email
    found_user = db.find_user_by(email="test@example.com")
    assert found_user is None, "User should not exist yet"

    # Add a user for testing
    db.add_user(email="test@example.com", hashed_password="password123")

    # Test finding non-existent user
    found_user = db.find_user_by(email="non_existent@example.com")
    assert found_user is None, "No user should be found for non-existent email"

    # Test finding user by non-existent attribute
    try:
        db.find_user_by(non_existent_attribute="value")
    except InvalidRequestError:
        pass  # InvalidRequestError should be raised
    else:
        assert False, "InvalidRequestError should be raised for wrong query arguments"

    print("All test cases passed successfully.")

if __name__ == "__main__":
    test_find_user_by()