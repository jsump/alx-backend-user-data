#!/usr/bin/env python3
"""
Module: auth.py
Authentication file
"""

import bcrypt
import uuid
import hashlib
from sqlalchemy.orm.exc import NoResultFound as NoResultFound_ORM
from typing import Any, Optional
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    This method in password string args and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
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
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound_ORM:
            pass

        hashed_password = _hash_password(password)
        new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login
        """
        user = self._db.find_user_by(email=email)

        if user:
            hashed_password = user.hashed_password
            provided_password = password.encode('utf-8')

            if bcrypt.checkpw(provided_password, hashed_password):
                return True
        return False

    def _generate_uuid() -> str:
        """
        This method generates a new UUID
        """
        try:
            return str(uuid.uuid4())
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def create_session(self, email: str) -> str:
        """
        This method creates a new session
        """
        user = self._db.find_user_by(email=email)
        if user:
            session_id = str(uuid.uuid4())
            self._db.store_session_id(user.id, session_id)
            return session_id
        else:
            raise ValueError("User not found")

    def get_user_from_session_id(self, session_id: str):
        """
        This method gets use fom session id
        """
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id)
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        This method destroys the session
        """
        self._db.update_session_id(user_id, None)

    def get_reset_password_token(self, email: str) -> str:
        """
        This method generated a UUID and update for user's
        reset token DB field and returns the token
        """
        user = self._db.find_user_by(email=email)

        if user is None:
            raise ValueError("User does not exist")
        token = str(uuid.uuid4())
        self._db.update_reset_token(user.id, token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        This method updates password
        """
        user = self._db.get_user_by_reset_token(reset_token)

        if user is None:
            raise ValueError("User does not exist")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self._db.update_password_And_reset_Token(
            user.id, hashed_password, None)
