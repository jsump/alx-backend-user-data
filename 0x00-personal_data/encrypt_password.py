#!/usr/bin/env python3
"""
Module: encrypt_password.py

Return salted, hashed password, which is a byte string
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Perform hashing with hashpw

    Expects one string argument name password
    Returns a salted, hashed password which is a byte string
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the arguments retrna aboolean
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
