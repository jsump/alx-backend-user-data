#!/usr/bin/env python3
"""
Module: app.py
Flask app
"""


from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def index():
    """
    this method returns the message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    This method implements the endpoint to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    This method checks if the login information is correct
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or password:
        abort(401)

    if AUTH.valid_login(email, password):
        response = make_response(
            jsonify({"email": email, "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)

@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    This method logs out the session
    """
    session_id = request.cookies.get('session_id')
    user = get_user_from_session_id(session_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
