#!/usr/bin/env python3
"""
Module: auth.py
This module contains a class for authentication
"""


from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    """
    This class contains methods on authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        THis method takes the path and exclused_paths as parameters
        Returns: False
        """
        return False
    
    def authorized_header(self, request=None) -> str:
        """
        This method takes an optional request parameter
        of flask bject header and returns None
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method takes in the current user as a parameter
        Return: None
        """
        return None