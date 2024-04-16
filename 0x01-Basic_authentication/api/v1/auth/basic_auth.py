#!/usr/bin/env python3
"""
Module: basic_auth.py

This module contains a class that inherits from Auth
"""


import base64
from models.user import User
from api.v1.auth.auth import Auth
from typing import TypeVar


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
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        This method returns the user instance based on
        the email and password
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        
        if user_email is None:
            return None


        try:
            users = User.search({'email': user_email})
        except User.DoesNotExist:
            return None
        
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method overloads Auth and retrieves the
        User instance for a request
        """
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_authorization_header is None:
            return None

        decoded_base64_authorization_header = \
            self.decode_base64_authorization_header(
                base64_authorization_header)
        if decoded_base64_authorization_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
