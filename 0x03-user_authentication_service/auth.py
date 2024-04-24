#!/usr/bin/env python3
"""
Module: auth.py
Authentication file
"""


import bcrypt
from typing import Any


def _hash_password(password: str) ->  bytes:
    """
    This method in password string args and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
