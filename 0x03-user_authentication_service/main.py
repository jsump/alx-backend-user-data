#!/usr/bin/env python3
"""
Main file
"""

import requests
import json


BASE_URL = " http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register user method
    """
    url = f"{BASE_URL}/register"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Registration failed"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Check wrong password method
    """
    url = f"{BASE_URL}/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401, "Unauthorized"


def log_in(email: str, password: str) -> str:
    """
    Log in method
    """
    url = f"{BASE_URL}/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Login failed"
    session_id = response.json()["session_id"]
    return session_id


def profile_unlogged() -> None:
    """
    Retrive user profile
    """
    url = f"{BASE_URL}/profile"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Unauthorized"


def profile_logged(session_id: str) -> None:
    """
    Retrive user profile
    """
    url = f"{BASE_URL}/profile"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Profile retrival failed"


def log_out() -> None:
    """
    Logout method
    """
    url = f"{BASE_URL}/logout"
    headers = {
        "Authorization": f"Bearer {session_id}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Logout failed"


def reset_password_token(email: str) -> str:
    """
    reset password method
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Password reset request failed"
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Password update method
    """
    url = f"{BASE_URL}/update_password"
    data = {
        "email": email,
        "new_password": new_password,
        "reset_token": reset_token
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Update password failed"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
