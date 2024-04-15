#!/usr/bin/env python3
"""
Module: basic_auth.py

This module contains a class that inherits from Auth
"""


import base64
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        This method returns the decoded value of Base64 string
        """
        if base64_authorization_header is None or not isinstance(
             base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        This method returns the user email and password from
        the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not \
            isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password 
