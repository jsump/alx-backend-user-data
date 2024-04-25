#!/usr/bin/env python3
"""
Module: auth.py
Authentication file
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Any
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    This method in password string args and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This method registers a new usre to the DB
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
        return new_user
