#!/usr/bin/env python3
"""
Module: auth.py
This module contains a class for authentication
"""


from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch


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
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if fnmatch(path, excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path.rstrip('/'):
                        return False
        return True

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        This method takes an optional request parameter
        of flask object header
        Return: None
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This method takes in the current user as a parameter
        Return: None
        """
        return None
