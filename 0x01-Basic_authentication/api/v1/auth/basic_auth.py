#!/usr/bin/env python3
"""
Module: basic_auth.py

This module contains a class that inherits from Auth
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    THis class inherits from Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        This method returns the Base64 part of the Authorization header
        for Basic Authentication
        """
        if authorization_header is None or not \
            isinstance(authorization_header, str) or not \
                authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
