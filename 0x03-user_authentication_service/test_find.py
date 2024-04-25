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

    # Add a user for testing
    db.add_user(email="test@example.com", hashed_password="password123")

    # Test finding user by valid keyword arguments
    found_user = db.find_user_by(email="test@example.com")
    assert found_user is not None, "User should be found"
    assert found_user.email == "test@example.com", "User email should match"

    # Test finding user by invalid keyword arguments
    try:
        db.find_user_by(non_existent_attribute="value")
    except InvalidRequestError:
        pass  # InvalidRequestError should be raised
    else:
        assert False, "InvalidRequestError should be raised for wrong query arguments"

    # Clear the database
    db._session.query(User).delete()
    db._session.commit()

    # Test finding non-existent user
    try:
        db.find_user_by(email="non_existent@example.com")
    except NoResultFound:
        pass  # NoResultFound should be raised
    else:
        assert False, "NoResultFound should be raised for non-existent user"

    print("All test cases passed successfully.")

if __name__ == "__main__":
    test_find_user_by()